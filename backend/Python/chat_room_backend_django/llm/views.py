"""
LLM views module for AI-powered chat room features.

This module provides views for:
- AI Admin: Generates responses based on worldview, character settings, and memory
- AI Actor: Handles character-based AI responses
- Memory Cleanup: Manages conversation history and short-term memory cleanup
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Count
import json
from typing import Dict, List, Any, Optional

from zai import ZhipuAiClient

from .models import (
    AdminRequest,
    ConversationHistory,
    ShortTermMemory
)


# Constants
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.7
AI_MODEL = "glm-4-plus"
MIN_DIALOGUES_THRESHOLD = 5
MAX_DIALOGUES_THRESHOLD = 10
MEMORY_CLEANUP_INTERVAL = 5
RECENT_MEMORIES_COUNT = 5
SYSTEM_PROMPT = (
    "你是一个专业的AI管理员，负责根据用户的世界观、人物设定和核心记忆，"
    "生成符合用户需求的回复。"
)


# ============================================================================
# Helper Functions
# ============================================================================

def parse_json_request(request_body: bytes) -> Dict[str, Any]:
    """Parse and validate JSON request body."""
    try:
        return json.loads(request_body)
    except json.JSONDecodeError:
        raise ValueError("无效的JSON格式")


def get_recent_dialogues(room_id: str) -> tuple[List[ConversationHistory], int]:
    """
    Get recent dialogues for a room based on memory cleanup logic.

    Rules:
    - Total <= 5: Return all dialogues
    - Total % 5 == 0: Return latest 5 dialogues (memory cleanup triggered)
    - Otherwise: Return latest 10 dialogues

    Returns:
        Tuple of (dialogues list, total count)
    """
    all_dialogues = ConversationHistory.objects.filter(room_id=room_id)
    total_dialogues = all_dialogues.count()

    if total_dialogues <= MIN_DIALOGUES_THRESHOLD:
        # Return all dialogues in chronological order
        recent_dialogues = list(all_dialogues.order_by('created_at'))
    elif total_dialogues % MEMORY_CLEANUP_INTERVAL == 0:
        # Memory cleanup triggered: get latest 5
        recent_dialogues = list(all_dialogues.order_by('-created_at')[:MIN_DIALOGUES_THRESHOLD])
        recent_dialogues.reverse()
    else:
        # Get latest 10 dialogues
        recent_dialogues = list(all_dialogues.order_by('-created_at')[:MAX_DIALOGUES_THRESHOLD])
        recent_dialogues.reverse()

    return recent_dialogues, total_dialogues


def get_recent_memories(room_id: str, limit: int = RECENT_MEMORIES_COUNT) -> List[ShortTermMemory]:
    """Get recent short-term memories for a room."""
    recent_memories = list(
        ShortTermMemory.objects.filter(room_id=room_id)
        .order_by('-created_at')[:limit]
    )
    recent_memories.reverse()
    return recent_memories


def build_core_memory(
    dialogues: List[ConversationHistory],
    memories: List[ShortTermMemory]
) -> List[Dict[str, Any]]:
    """Build core memory from dialogues and short-term memories."""
    core_memory = []

    # Add dialogues to core memory
    for dialogue in dialogues:
        core_memory.append({
            'type': 'dialogue',
            'character_id': dialogue.character_id,
            'character_name': dialogue.character_name,
            'content': dialogue.content,
            'location': dialogue.current_location,
            'status': dialogue.status,
            'timestamp': dialogue.created_at.isoformat()
        })

    # Add short-term memories to core memory
    for memory in memories:
        core_memory.append({
            'type': 'memory',
            'content': memory.content,
            'timestamp': memory.created_at.isoformat()
        })

    return core_memory


def build_prompt(
    worldview: str,
    character_settings: List[str],
    core_memory: List[Dict[str, Any]]
) -> str:
    """Build the prompt for AI model."""
    prompt_parts = [
        f"世界观: {worldview}",
        "人物设定:"
    ]

    # Add character settings
    for setting in character_settings:
        prompt_parts.append(f"- {setting}")

    prompt_parts.append("\n核心记忆:")

    # Add core memory
    for item in core_memory:
        if item['type'] == 'dialogue':
            prompt_parts.append(
                f"[{item['timestamp']}] {item['character_name']}({item['character_id']}) "
                f"[{item['location']}] [{item['status']}]: {item['content']}"
            )
        else:
            prompt_parts.append(f"[{item['timestamp']}] [记忆]: {item['content']}")

    prompt_parts.append("\n请根据以上信息，以AI管理员的身份生成适当的回复。")

    return "\n".join(prompt_parts)


def call_ai_model(prompt: str) -> str:
    """Call Zhipu AI model and return the response."""
    client = ZhipuAiClient(api_key=settings.ZHIPU_API_KEY)
    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=DEFAULT_MAX_TOKENS,
        temperature=DEFAULT_TEMPERATURE
    )
    return response.choices[0].message.content


def json_error_response(error_message: str, status: int = 400) -> JsonResponse:
    """Create a JSON error response."""
    return JsonResponse({"error": error_message}, status=status)


def method_not_allowed_response() -> JsonResponse:
    """Create a method not allowed response."""
    return JsonResponse({"error": "只支持POST请求"}, status=405)


# ============================================================================
# View Functions
# ============================================================================

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

        # Call AI model
        ai_response = call_ai_model(prompt)

        # Return response
        return JsonResponse({
            "message": "AI管理员接口已处理请求",
            "roomId": admin_request.roomId,
            "characterId": admin_request.characterId,
            "core_memory": core_memory,
            "prompt": prompt,
            "ai_response": ai_response,
            "total_dialogues": total_dialogues
        })

    except ValueError as e:
        return json_error_response(str(e), 400)
    except Exception as e:
        return json_error_response(str(e), 500)


@csrf_exempt
def ai_actor(request):
    """
    AI Actor endpoint.

    Handles character-based AI responses.
    TODO: Implement actual logic.

    POST /llm/ai-actor/
    """
    if request.method != 'POST':
        return method_not_allowed_response()

    return JsonResponse({"message": "AI扮演者接口已接收POST请求"})


@csrf_exempt
def memory_cleanup(request):
    """
    Memory Cleanup endpoint.

    Manages conversation history and short-term memory cleanup.
    TODO: Implement actual cleanup logic.

    POST /llm/memory-cleanup/
    Body:
        room_id (str): The room ID to cleanup memories for
    """
    if request.method != 'POST':
        return method_not_allowed_response()

    try:
        request_data = parse_json_request(request.body)
        room_id = request_data.get('room_id')

        if not room_id:
            return json_error_response("room_id参数是必需的", 400)

        # TODO: Implement memory cleanup logic
        return JsonResponse({
            "message": "记忆整理接口已处理请求",
            "room_id": room_id,
            "status": "success"
        })

    except ValueError as e:
        return json_error_response(str(e), 400)
    except Exception as e:
        return json_error_response(str(e), 500)
