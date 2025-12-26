"""
Constants for LLM views module.
"""

from typing import Dict, Any

# AI Model Configuration
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.7
AI_MODEL = "glm-4.6"

# Memory Configuration
MAX_DIALOGUES_THRESHOLD = 10
RECENT_MEMORIES_COUNT = 5

# System Prompts
SYSTEM_PROMPT = (
    "你是一个专业的AI管理员，负责根据用户的世界观、人物设定和核心记忆，"
    "生成符合用户需求的回复。\n\n"
    "重要：你必须使用提供的工具函数来返回你的分析结果，而不是直接输出文本。"
)

ACTOR_SYSTEM_PROMPT_TEMPLATE = (
    "你现在要扮演角色【{character_name}】，请根据以下信息进行角色扮演：\n"
    "1. 世界观设定\n"
    "2. 角色设定\n"
    "3. 核心记忆（历史对话和短期记忆）\n\n"
    "请完全沉浸在【{character_name}】这个角色中，根据角色的性格、说话风格和当前状态，"
    "结合历史对话的上下文，生成符合角色设定的回复。\n\n"
    "重要：你必须使用提供的工具函数来返回你的回复，而不是直接输出文本。"
)

# Function Call Tools
ADMIN_TOOL: Dict[str, Any] = {
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

ACTOR_TOOL: Dict[str, Any] = {
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
