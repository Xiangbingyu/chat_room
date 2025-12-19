from django.db import models
import uuid
from typing import List, Dict, Optional
from pydantic import BaseModel


# Django ORM Models

class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['username']),
        ]


class Rooms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False)
    worldview = models.TextField(null=False)
    location = models.JSONField(null=True)
    creator_id = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='creator_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rooms'
        indexes = [
            models.Index(fields=['created_at']),
        ]


class Characters(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    room_id = models.ForeignKey(Rooms, on_delete=models.CASCADE, db_column='room_id')
    current_location = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=50, null=True)
    type = models.CharField(max_length=20, default='user', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'characters'
        indexes = [
            models.Index(fields=['room_id']),
        ]


class Conversations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_id = models.ForeignKey(Rooms, on_delete=models.CASCADE, db_column='room_id')
    character_id = models.ForeignKey(Characters, on_delete=models.CASCADE, db_column='character_id')
    content = models.TextField(null=False)
    current_location = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=50, null=True)
    next_speaker = models.ForeignKey(Characters, on_delete=models.SET_NULL, null=True, related_name='next_speaker')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conversations'
        indexes = [
            models.Index(fields=['room_id', 'created_at']),
        ]


class ShortTermMemories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(null=False)
    room_id = models.ForeignKey(Rooms, on_delete=models.CASCADE, db_column='room_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'short_term_memories'
        indexes = [
            models.Index(fields=['room_id', 'created_at']),
        ]


class LongTermMemories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(null=False)
    embedding = models.BinaryField(null=False)  # SQLite VEC type will be handled during migration
    room_id = models.ForeignKey(Rooms, on_delete=models.CASCADE, db_column='room_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'long_term_memories'
        indexes = [
            models.Index(fields=['room_id']),
        ]


class ConversationHistories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(null=False)
    room_id = models.ForeignKey(Rooms, on_delete=models.CASCADE, db_column='room_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conversation_histories'
        indexes = [
            models.Index(fields=['room_id', 'created_at']),
        ]


# Pydantic Models for API

# AI管理员接口 - 请求数据格式
class AdminRequest(BaseModel):
    roomId: str  # 房间ID
    characterId: str  # 角色ID
    history_dialogues: str  # 上一句的回复内容
    character_settings: List[str]  # 人物设定列表
    worldview: str  # 世界观描述


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
