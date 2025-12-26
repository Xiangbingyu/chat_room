from django.contrib import admin
from .models.db_models import (
    ShortTermMemory,
    LongTermMemory,
    ConversationHistory,
    AdminAnalysisRecord
)

admin.site.register(ShortTermMemory)
admin.site.register(LongTermMemory)
admin.site.register(ConversationHistory)
admin.site.register(AdminAnalysisRecord)
