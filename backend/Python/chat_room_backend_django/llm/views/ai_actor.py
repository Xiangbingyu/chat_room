"""
AI Actor view module.

Handles character-based AI responses.
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import ActorRequest, ConversationHistory
from .utils import (
    parse_json_request,
    get_recent_dialogues,
    get_recent_memories,
    build_core_memory,
    build_prompt,
    call_ai_model,
    ACTOR_SYSTEM_PROMPT_TEMPLATE,
    ACTOR_TOOL,
    json_error_response,
    method_not_allowed_response
)


@csrf_exempt
def ai_actor(request):
    """
    AI Actor endpoint.

    Handles character-based AI responses based on:
    - Worldview
    - Character settings
    - Core memory (dialogues + short-term memories)

    POST /llm/ai-actor/
    """
    if request.method != 'POST':
        return method_not_allowed_response()

    try:
        # Parse and validate request
        request_data = parse_json_request(request.body)
        actor_request = ActorRequest(**request_data)

        # Save current conversation to history
        conversation = ConversationHistory(
            room_id=actor_request.roomId,
            character_id=actor_request.previous_speaker_id,
            character_name=actor_request.previous_speaker_name,
            content=actor_request.history_dialogues,
            current_location=actor_request.previous_speaker_location,
            status=actor_request.previous_speaker_status
        )
        conversation.save()

        # Get recent dialogues and memories
        recent_dialogues, total_dialogues = get_recent_dialogues(actor_request.roomId)
        recent_memories = get_recent_memories(actor_request.roomId)

        # Build core memory
        core_memory = build_core_memory(recent_dialogues, recent_memories)

        # Build prompt for AI model
        prompt = build_prompt(
            actor_request.worldview,
            actor_request.character_settings,
            core_memory,
            actor_request.character_name
        )

        # Build system prompt for role-playing
        system_prompt = ACTOR_SYSTEM_PROMPT_TEMPLATE.format(
            character_name=actor_request.character_name
        )

        # Call AI model with role-playing system prompt and function call tool
        ai_result = call_ai_model(
            prompt,
            system_prompt,
            tools=[ACTOR_TOOL],
            tool_choice="required"
        )

        # Extract tool call result
        if ai_result["type"] == "tool_call":
            tool_args = ai_result["tool_arguments"]
            ai_response_content = tool_args.get("response_content", "")
            actor_character_name = tool_args.get("character_name", actor_request.character_name)
            actor_current_location = tool_args.get("current_location", actor_request.current_location)
            actor_status = tool_args.get("status", actor_request.status)
        else:
            ai_response_content = ai_result.get("content", "")
            actor_character_name = actor_request.character_name
            actor_current_location = actor_request.current_location
            actor_status = actor_request.status

        # Save AI actor response to conversation history
        actor_conversation = ConversationHistory(
            room_id=actor_request.roomId,
            character_id=actor_request.characterId,
            character_name=actor_character_name,
            content=ai_response_content,
            current_location=actor_current_location,
            status=actor_status
        )
        actor_conversation.save()

        # Return response
        return JsonResponse({
            "message": "AI扮演者接口已处理请求",
            "roomId": actor_request.roomId,
            "characterId": actor_request.characterId,
            "character_name": actor_character_name,
            "current_location": actor_current_location,
            "status": actor_status,
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