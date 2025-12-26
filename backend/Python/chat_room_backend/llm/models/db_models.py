from django.db import models
from django.utils import timezone
import uuid


def generate_uuid():
    return str(uuid.uuid4())


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


class LongTermMemory(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=generate_uuid)
    room_id = models.CharField(max_length=36, db_index=True)
    content = models.TextField()
    embedding = models.BinaryField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'long_term_memories'
        indexes = [
            models.Index(fields=['room_id']),
        ]


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
