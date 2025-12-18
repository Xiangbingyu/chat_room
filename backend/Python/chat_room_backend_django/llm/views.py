from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def ai_admin(request):
    if request.method == 'POST':
        # 只保留POST请求处理，不实现具体逻辑
        return JsonResponse({"message": "AI管理员接口已接收POST请求"})
    else:
        return JsonResponse({"error": "只支持POST请求"}, status=405)


@csrf_exempt
def ai_actor(request):
    if request.method == 'POST':
        # 只保留POST请求处理，不实现具体逻辑
        return JsonResponse({"message": "AI扮演者接口已接收POST请求"})
    else:
        return JsonResponse({"error": "只支持POST请求"}, status=405)
