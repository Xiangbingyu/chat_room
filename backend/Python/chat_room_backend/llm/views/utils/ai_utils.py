"""
AI model utilities for LLM views module.
"""

import json
from typing import Dict, Any, Optional, List
from django.conf import settings
from zai import ZhipuAiClient

from .constants import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    AI_MODEL,
    SYSTEM_PROMPT
)


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
