from django.urls import path
from .views import ai_admin, ai_actor, memory_cleanup

urlpatterns = [
    path('api/ai/admin', ai_admin, name='ai_admin'),
    path('api/ai/actor', ai_actor, name='ai_actor'),
    path('api/memory/cleanup', memory_cleanup, name='memory_cleanup'),
]
