"""
Memory Cleanup view module.

Manages conversation history and short-term memory cleanup.
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import parse_json_request, json_error_response, method_not_allowed_response


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