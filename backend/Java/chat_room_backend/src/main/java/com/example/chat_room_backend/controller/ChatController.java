package com.example.chat_room_backend.controller;

import com.example.chat_room_backend.entity.Conversations;
import com.example.chat_room_backend.service.ConversationsService;
import com.example.chat_room_backend.service.WebSocketClientService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.messaging.simp.SimpMessageHeaderAccessor;
import org.springframework.stereotype.Controller;

import java.util.Map;

/**
 * WebSocket控制器，处理实时聊天消息
 */
@Controller
public class ChatController {

    @Autowired
    private ConversationsService conversationsService;

    @Autowired
    private WebSocketClientService webSocketClientService;

    /**
     * 发送消息到房间
     * 客户端发送消息到：/app/chat/{roomId}
     * 服务器将消息广播到：/topic/chat/{roomId}
     */
    @MessageMapping("/chat/{roomId}")
    @SendTo("/topic/chat/{roomId}")
    public Conversations sendMessage(@DestinationVariable String roomId, Map<String, Object> message, SimpMessageHeaderAccessor headerAccessor) {
        // 从消息中提取参数
        String characterId = (String) message.get("characterId");
        String content = (String) message.get("content");
        String location = (String) message.get("location");
        String status = (String) message.get("status");
        String nextSpeaker = (String) message.get("next_speaker");

        // 创建/更新对话
        Conversations conversation = conversationsService.createOrUpdateConversation(
                roomId, characterId, content, location, status, nextSpeaker
        );

        // 如果下一个说话者是AI角色，则触发AI调用逻辑
        if (isAICharacter(nextSpeaker)) {
            // 构造消息格式，发送给Python后端
            String newMessage = String.format("{\"roomId\":\"%s\",\"characterId\":\"%s\",\"content\":\"%s\",\"location\":\"%s\",\"status\":\"%s\",\"nextSpeaker\":\"%s\"}",
                    roomId, characterId, content, location, status, nextSpeaker);

            // 调用WebSocket客户端发送消息到Python后端
            webSocketClientService.sendMessageToPython(newMessage);
        }

        // 返回对话信息，会自动广播到/topic/chat/{roomId}频道
        return conversation;
    }

    /**
     * 判断是否是AI角色
     */
    private boolean isAICharacter(String characterId) {
        // 这里可以根据实际业务逻辑判断是否是AI角色
        // 例如，可以根据characterId的前缀或其他标识来判断
        return characterId != null && characterId.startsWith("ai_");
    }

    /**
     * 加入房间
     * 客户端发送消息到：/app/chat/join/{roomId}
     * 服务器将欢迎消息广播到：/topic/chat/{roomId}
     */
    @MessageMapping("/chat/join/{roomId}")
    @SendTo("/topic/chat/{roomId}")
    public Map<String, Object> joinRoom(@DestinationVariable String roomId, Map<String, String> message) {
        String userId = message.get("userId");
        String userName = message.get("userName");

        // 创建欢迎消息
        return Map.of(
                "type", "system",
                "message", userName + " 加入了房间",
                "roomId", roomId,
                "userId", userId,
                "timestamp", System.currentTimeMillis()
        );
    }

    /**
     * 离开房间
     * 客户端发送消息到：/app/chat/leave/{roomId}
     * 服务器将离开消息广播到：/topic/chat/{roomId}
     */
    @MessageMapping("/chat/leave/{roomId}")
    @SendTo("/topic/chat/{roomId}")
    public Map<String, Object> leaveRoom(@DestinationVariable String roomId, Map<String, String> message) {
        String userId = message.get("userId");
        String userName = message.get("userName");

        // 创建离开消息
        return Map.of(
                "type", "system",
                "message", userName + " 离开了房间",
                "roomId", roomId,
                "userId", userId,
                "timestamp", System.currentTimeMillis()
        );
    }
}
