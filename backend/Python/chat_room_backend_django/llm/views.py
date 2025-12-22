from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import AdminRequest, ConversationHistory, ShortTermMemory
from django.db.models import Count


@csrf_exempt
def ai_admin(request):
    if request.method == 'POST':
        try:
            # 解析请求体
            request_data = json.loads(request.body)
            
            # 验证请求数据格式
            admin_request = AdminRequest(**request_data)
            
            # 1. 保存请求数据到ConversationHistories
            conversation = ConversationHistory(
                room_id=admin_request.roomId,
                character_id=admin_request.previous_speaker_id,
                character_name=admin_request.previous_speaker_name,
                content=admin_request.history_dialogues,
                current_location=admin_request.previous_speaker_location,
                status=admin_request.previous_speaker_status
            )
            conversation.save()
            
            # 2. 从ConversationHistories中提取该房间近5-10条对话
            # 获取该房间的总对话数
            all_dialogues = ConversationHistory.objects.filter(
                room_id=admin_request.roomId
            ).order_by('created_at')  # 正序：最早→最新
            total_dialogues = all_dialogues.count()
            
            # 计算需要提取的对话数量（5-10条）
            if total_dialogues <= 5:
                # 总对话≤5条：取全部（保证至少1条，符合“5条基础”的最低要求）
                recent_dialogues = all_dialogues  # 正序
            elif total_dialogues % 5 == 0:
                # 每5轮对话触发记忆整理，提取最新的5条
                recent_dialogues = all_dialogues.order_by('-created_at')[:5].order_by('created_at')
            else:
                # 否则提取最新的5-10条
                # 核心记忆最多10条，当超过10条且未到整理时机时，提取最新的10条
                recent_dialogues = all_dialogues.order_by('-created_at')[:10].order_by('created_at')  # 转回正序
            
            # 反转顺序，确保对话按时间顺序排列
            recent_dialogues = list(recent_dialogues)[::-1]
            
            # 3. 从ShortTermMemories提取近5段对话
            recent_memories = ShortTermMemory.objects.filter(
                room_id=admin_request.roomId
            ).order_by('-created_at')[:5]
            
            # 提取近5条短期记忆（正序）
            recent_memories = ShortTermMemory.objects.filter(
                room_id=admin_request.roomId
            ).order_by('-created_at')[:5].order_by('created_at')  # 转回正序
            
            # 4. 形成最终的核心记忆
            core_memory = []
            
            # 添加对话历史到核心记忆
            for dialogue in recent_dialogues:
                core_memory.append({
                    'type': 'dialogue',
                    'character_id': dialogue.character_id,
                    'character_name': dialogue.character_name,
                    'content': dialogue.content,
                    'location': dialogue.current_location,
                    'status': dialogue.status,
                    'timestamp': dialogue.created_at.isoformat()
                })
            
            # 添加短期记忆到核心记忆
            for memory in recent_memories:
                core_memory.append({
                    'type': 'memory',
                    'content': memory.content,
                    'timestamp': memory.created_at.isoformat()
                })
            
            # 5. 整理为prompt
            prompt = f"""
世界观: {admin_request.worldview}

人物设定:
"""
            
            # 添加人物设定
            for setting in admin_request.character_settings:
                prompt += f"- {setting}\n"
            
            prompt += "\n核心记忆:\n"
            
            # 添加核心记忆
            for item in core_memory:
                if item['type'] == 'dialogue':
                    prompt += f"[{item['timestamp']}] {item['character_name']}({item['character_id']}) [{item['location']}] [{item['status']}]: {item['content']}\n"
                else:
                    prompt += f"[{item['timestamp']}] [记忆]: {item['content']}\n"
            
            prompt += "\n请根据以上信息，以AI管理员的身份生成适当的回复。"
            
            # 6. 返回处理结果（不包含实际的大模型调用结果）
            return JsonResponse({
                "message": "AI管理员接口已处理请求",
                "roomId": admin_request.roomId,
                "characterId": admin_request.characterId,
                "core_memory": core_memory,
                "prompt": prompt,
                "total_dialogues": total_dialogues
            })
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "无效的JSON格式"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "只支持POST请求"}, status=405)


@csrf_exempt
def ai_actor(request):
    if request.method == 'POST':
        # 只保留POST请求处理，不实现具体逻辑
        return JsonResponse({"message": "AI扮演者接口已接收POST请求"})
    else:
        return JsonResponse({"error": "只支持POST请求"}, status=405)
