"""
Utility functions for LLM views module.
"""

from django.http import JsonResponse
from django.conf import settings
from django.db.models import Count
import json
from typing import Dict, List, Any, Optional

from zai import ZhipuAiClient

from ..models import (
    ConversationHistory,
    ShortTermMemory
)


# Constants
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.7
AI_MODEL = "glm-4-plus"
MAX_DIALOGUES_THRESHOLD = 10
RECENT_MEMORIES_COUNT = 5
SYSTEM_PROMPT = (
    "你是一个专业的AI管理员，负责根据用户的世界观、人物设定和核心记忆，"
    "生成符合用户需求的回复。\n\n"
    "重要：你必须使用提供的工具函数来返回你的分析结果，而不是直接输出文本。"
)

ADMIN_TOOL = {
    "type": "function",
    "function": {
        "name": "admin_analysis",
        "description": "AI管理员的分析结果",
        "parameters": {
            "type": "object",
            "properties": {
                "analysis_content": {
                    "type": "string",
                    "description": "管理员分析内容"
                },
                "next_speaker": {
                    "type": "string",
                    "description": "下一个说话的人物名字"
                }
            },
            "required": ["analysis_content", "next_speaker"]
        }
    }
}

ACTOR_SYSTEM_PROMPT_TEMPLATE = (
    "你现在要扮演角色【{character_name}】，请根据以下信息进行角色扮演：\n"
    "1. 世界观设定\n"
    "2. 角色设定\n"
    "3. 核心记忆（历史对话和短期记忆）\n\n"
    "请完全沉浸在【{character_name}】这个角色中，根据角色的性格、说话风格和当前状态，"
    "结合历史对话的上下文，生成符合角色设定的回复。\n\n"
    "重要：你必须使用提供的工具函数来返回你的回复，而不是直接输出文本。"
)

ACTOR_TOOL = {
    "type": "function",
    "function": {
        "name": "actor_response",
        "description": "AI扮演者的回复信息",
        "parameters": {
            "type": "object",
            "properties": {
                "character_name": {
                    "type": "string",
                    "description": "AI扮演者所扮演的人物姓名"
                },
                "response_content": {
                    "type": "string",
                    "description": "AI扮演者具体回复内容"
                },
                "current_location": {
                    "type": "string",
                    "description": "该人物目前位置"
                },
                "status": {
                    "type": "string",
                    "description": "该人物目前状态"
                },
                "next_speaker": {
                    "type": "string",
                    "description": "下一个说话的人物名字"
                }
            },
            "required": ["character_name", "response_content", "current_location", "status", "next_speaker"]
        }
    }
}


def parse_json_request(request_body: bytes) -> Dict[str, Any]:
    """Parse and validate JSON request body."""
    try:
        return json.loads(request_body)
    except json.JSONDecodeError:
        raise ValueError("无效的JSON格式")


def get_recent_dialogues(room_id: str) -> tuple[List[ConversationHistory], int]:
    """
    Get recent dialogues for a room.

    Returns the latest 10 dialogues in chronological order.

    Returns:
        Tuple of (dialogues list, total count)
    """
    all_dialogues = ConversationHistory.objects.filter(room_id=room_id)
    total_dialogues = all_dialogues.count()

    # Get latest 10 dialogues in chronological order
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
    core_memory: List[Dict[str, Any]],
    character_name: Optional[str] = None
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

    if character_name:
        prompt_parts.append(f"\n请根据以上信息，以【{character_name}】的身份生成适当的回复。")
    else:
        prompt_parts.append("\n请根据以上信息，以AI管理员的身份生成适当的回复。")

    return "\n".join(prompt_parts)


def call_ai_model(
    prompt: str,
    system_prompt: Optional[str] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_choice: Optional[str] = None
) -> Dict[str, Any]:
    """Call Zhipu AI model and return the response."""
    if system_prompt is None:
        system_prompt = SYSTEM_PROMPT
    
    client = ZhipuAiClient(api_key=settings.ZHIPU_API_KEY)
    
    request_params = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": DEFAULT_MAX_TOKENS,
        "temperature": DEFAULT_TEMPERATURE
    }
    
    if tools is not None:
        request_params["tools"] = tools
    
    if tool_choice is not None:
        request_params["tool_choice"] = tool_choice
    
    response = client.chat.completions.create(**request_params)
    
    message = response.choices[0].message
    
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        return {
            "type": "tool_call",
            "tool_name": tool_call.function.name,
            "tool_arguments": json.loads(tool_call.function.arguments)
        }
    else:
        return {
            "type": "text",
            "content": message.content
        }


def json_error_response(error_message: str, status: int = 400) -> JsonResponse:
    """Create a JSON error response."""
    return JsonResponse({"error": error_message}, status=status)


def method_not_allowed_response() -> JsonResponse:
    """Create a method not allowed response."""
    return JsonResponse({"error": "只支持POST请求"}, status=405)