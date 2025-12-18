package com.example.chat_room_backend.service;

import com.example.chat_room_backend.entity.Conversations;
import java.util.List;

public interface ConversationsService {
    // 获取房间内所有对话
    List<Conversations> getConversationsByRoomId(String roomId);
    
    // 根据ID获取对话详情
    Conversations getConversationById(String conversationId);
    
    // 创建/更新对话
    Conversations createOrUpdateConversation(String roomId, String characterId, String content, String currentLocation, String status, String nextSpeaker);
    
    // 更新对话信息
    boolean updateConversation(Conversations conversation);
}