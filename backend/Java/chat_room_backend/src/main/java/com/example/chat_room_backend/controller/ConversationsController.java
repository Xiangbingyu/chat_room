package com.example.chat_room_backend.controller;

import com.example.chat_room_backend.entity.Conversations;
import com.example.chat_room_backend.service.ConversationsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/conversations")
public class ConversationsController {
    
    @Autowired
    private ConversationsService conversationsService;
    
    /**
     * 获取房间内所有对话
     */
    @GetMapping
    public ResponseEntity<?> getConversationsByRoomId(@RequestParam String roomId) {
        try {
            List<Conversations> conversations = conversationsService.getConversationsByRoomId(roomId);
            return ResponseEntity.ok(conversations);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("获取对话列表失败: " + e.getMessage());
        }
    }
    
    /**
     * 创建/更新对话记录
     */
    @PostMapping
    public ResponseEntity<?> createOrUpdateConversation(@RequestBody Map<String, Object> requestBody) {
        String roomId = (String) requestBody.get("roomId");
        String characterId = (String) requestBody.get("characterId");
        String content = (String) requestBody.get("content");
        // 同时支持current_location和currentLocation两种命名方式
        String currentLocation = (String) requestBody.get("current_location");
        if (currentLocation == null) {
            currentLocation = (String) requestBody.get("currentLocation");
        }
        String status = (String) requestBody.get("status");
        String nextSpeaker = (String) requestBody.get("next_speaker");
        
        // 参数校验
        if (roomId == null || roomId.isEmpty() || characterId == null || characterId.isEmpty() || content == null || content.isEmpty()) {
            return ResponseEntity.badRequest().body("房间ID、角色ID和对话内容不能为空");
        }
        
        try {
            // 调用服务层创建/更新对话
            Conversations conversation = conversationsService.createOrUpdateConversation(
                roomId, characterId, content, currentLocation, status, nextSpeaker
            );
            
            // 返回对话信息
            return ResponseEntity.status(HttpStatus.CREATED).body(Map.of(
                "id", conversation.getId(),
                "room_id", conversation.getRoomId(),
                "character_id", conversation.getCharacterId(),
                "character_name", conversation.getCharacterName(),
                "content", conversation.getContent(),
                "current_location", conversation.getCurrentLocation(),
                "status", conversation.getStatus(),
                "next_speaker", conversation.getNextSpeaker(),
                "created_at", conversation.getCreatedAt()
            ));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("创建对话失败: " + e.getMessage());
        }
    }
}