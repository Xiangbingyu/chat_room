"""
AI Admin view module.

Handles AI admin responses based on worldview, character settings, and memory.
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import AdminRequest, ConversationHistory, AdminAnalysisRecord
from .utils import (
    parse_json_request,
    get_recent_dialogues,
    get_recent_memories,
    build_core_memory,
    build_prompt,
    call_ai_model,
    ADMIN_TOOL,
    json_error_response,
    method_not_allowed_response
)


@csrf_exempt
def ai_admin(request):
    """
    AI Admin endpoint.

    Processes requests to generate AI admin responses based on:
    - Worldview
    - Character settings
    - Core memory (dialogues + short-term memories)

    POST /llm/ai-admin/
    """
    if request.method != 'POST':
        return method_not_allowed_response()

    try:
        # Parse and validate request
        request_data = parse_json_request(request.body)
        admin_request = AdminRequest(**request_data)

        # Save current conversation to history
        conversation = ConversationHistory(
            room_id=admin_request.roomId,
            character_id=admin_request.previous_speaker_id,
            character_name=admin_request.previous_speaker_name,
            content=admin_request.history_dialogues,
            current_location=admin_request.previous_speaker_location,
            status=admin_request.previous_speaker_status
        )
        conversation.save()

        # Get recent dialogues and memories
        recent_dialogues, total_dialogues = get_recent_dialogues(admin_request.roomId)
        recent_memories = get_recent_memories(admin_request.roomId)

        # Build core memory
        core_memory = build_core_memory(recent_dialogues, recent_memories)

        # Build prompt for AI model
        prompt = build_prompt(
            admin_request.worldview,
            admin_request.character_settings,
            core_memory
        )

        # Call AI model with function call tool
        ai_result = call_ai_model(
            prompt,
            tools=[ADMIN_TOOL],
            tool_choice="required"
        )

        # Extract tool call result
        if ai_result["type"] == "tool_call":
            tool_args = ai_result["tool_arguments"]
            ai_response_content = tool_args.get("analysis_content", "")
        else:
            ai_response_content = ai_result.get("content", "")

        # Save AI admin analysis to admin analysis record
        admin_analysis = AdminAnalysisRecord(
            room_id=admin_request.roomId,
            character_id=admin_request.characterId,
            analysis_content=ai_response_content
        )
        admin_analysis.save()

        # Return response
        return JsonResponse({
            "message": "AI管理员接口已处理请求",
            "roomId": admin_request.roomId,
            "characterId": admin_request.characterId,
            "core_memory": core_memory,
            "prompt": prompt,
            "ai_response": ai_response_content,
            "ai_result": ai_result,
            "total_dialogues": total_dialogues
        })

    except ValueError as e:
        return json_error_response(str(e), 400)
    except Exception as e:
        return json_error_response(str(e), 500)