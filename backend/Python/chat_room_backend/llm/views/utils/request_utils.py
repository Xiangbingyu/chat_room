"""
Request and response utilities for LLM views module.
"""

import json
from typing import Dict, Any
from django.http import JsonResponse


def parse_json_request(request_body: bytes) -> Dict[str, Any]:
    """Parse and validate JSON request body."""
    try:
        return json.loads(request_body)
    except json.JSONDecodeError:
        raise ValueError("无效的JSON格式")


def json_error_response(error_message: str, status: int = 400) -> JsonResponse:
    """Create a JSON error response."""
    return JsonResponse({"error": error_message}, status=status)


def method_not_allowed_response() -> JsonResponse:
    """Create a method not allowed response."""
    return JsonResponse({"error": "只支持POST请求"}, status=405)
