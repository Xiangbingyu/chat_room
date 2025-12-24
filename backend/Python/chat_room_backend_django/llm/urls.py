from django.urls import path
from . import views

urlpatterns = [
    path('api/ai/admin', views.ai_admin, name='ai_admin'),
    path('api/ai/actor', views.ai_actor, name='ai_actor'),
    path('api/memory/cleanup', views.memory_cleanup, name='memory_cleanup'),
]
