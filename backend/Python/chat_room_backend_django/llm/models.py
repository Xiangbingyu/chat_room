from typing import List, Dict, Optional
from pydantic import BaseModel
from django.db import models
from django.utils import timezone
import uuid


# AI管理员接口 - 请求数据格式
class AdminRequest(BaseModel):
    roomId: str  # 房间ID
    characterId: str  # 角色ID
    history_dialogues: str  # 上一句的回复内容
    character_settings: List[str]  # 人物设定列表
    worldview: str  # 世界观描述
    previous_speaker_id: str  # 上一轮说话角色的ID
    previous_speaker_name: str  # 上一轮说话角色的姓名
    previous_speaker_location: str  # 上一轮对话的地点
    previous_speaker_status: str  # 上一轮对话的状态


# AI管理员接口 - 响应数据格式
class AdminResponse(BaseModel):
    roomId: str  # 房间ID
    characterId: str  # 角色ID
    response_content: str  # 管理员回复内容
    next_speaker: str  # 下一轮对话角色


# AI扮演者接口 - 请求数据格式
class ActorRequest(BaseModel):
    roomId: str  # 房间ID
    characterId: str  # 角色ID
    history_dialogues: str  # 上一句的回复内容
    character_settings: List[str]  # 人物设定列表
    worldview: str  # 世界观描述
    character_name: str  # 扮演的角色名称
    current_location: str  # 对话发生地点
    status: str  # 对话状态

# AI扮演者接口 - 响应数据格式
class ActorResponse(BaseModel):
    roomId: str  # 房间ID
    characterId: str  # 角色ID
    response_content: str  # 角色回复内容
    next_speaker: str  # 下一轮对话角色
    current_location: str  # 对话发生地点
    status: str  # 对话状态


# 生成UUID的辅助函数
def generate_uuid():
    return str(uuid.uuid4())


# 数据库模型 - 短期记忆表
class ShortTermMemory(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=generate_uuid)
    room_id = models.CharField(max_length=36, db_index=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'short_term_memories'
        indexes = [
            models.Index(fields=['room_id', 'created_at']),
        ]

# 数据库模型 - 长期记忆表
class LongTermMemory(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=generate_uuid)
    room_id = models.CharField(max_length=36, db_index=True)
    content = models.TextField()
    # 使用BinaryField存储向量数据，后续通过sqlite-vec扩展处理
    embedding = models.BinaryField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'long_term_memories'
        indexes = [
            models.Index(fields=['room_id']),
        ]

# 数据库模型 - 历史对话表
class ConversationHistory(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=generate_uuid)
    room_id = models.CharField(max_length=36, db_index=True)
    character_id = models.CharField(max_length=36, db_index=True)
    character_name = models.CharField(max_length=50)
    content = models.TextField()
    current_location = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conversation_histories'
        indexes = [
            models.Index(fields=['room_id', 'created_at']),
            models.Index(fields=['room_id', 'character_id']),
        ]

# 数据库模型 - AI管理员分析记录表
class AdminAnalysisRecord(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=generate_uuid)
    room_id = models.CharField(max_length=36, db_index=True)
    character_id = models.CharField(max_length=36, db_index=True)
    analysis_content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_analysis_records'
        indexes = [
            models.Index(fields=['room_id', 'created_at']),
            models.Index(fields=['room_id', 'character_id']),
        ]
