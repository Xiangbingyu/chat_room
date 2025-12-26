"""
Prompt utilities for LLM views module.
"""

from typing import List, Dict, Any, Optional


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
