package com.example.chat_room_backend.controller;

import com.example.chat_room_backend.entity.Characters;
import com.example.chat_room_backend.service.CharactersService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/characters")
public class CharactersController {
    
    @Autowired
    private CharactersService charactersService;
    
    /**
     * 获取房间内所有角色
     */
    @GetMapping
    public ResponseEntity<?> getCharactersByRoomId(@RequestParam String roomId) {
        try {
            List<Characters> characters = charactersService.getCharactersByRoomId(roomId);
            return ResponseEntity.ok(characters);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("获取角色列表失败: " + e.getMessage());
        }
    }
    
    /**
     * 创建角色
     */
    @PostMapping
    public ResponseEntity<?> createCharacter(@RequestBody Map<String, Object> requestBody) {
        String roomId = (String) requestBody.get("roomId");
        String name = (String) requestBody.get("name");
        String description = (String) requestBody.get("description");
        // 同时支持current_location和currentLocation两种命名方式
        String currentLocation = (String) requestBody.get("current_location");
        if (currentLocation == null) {
            currentLocation = (String) requestBody.get("currentLocation");
        }
        String status = (String) requestBody.get("status");
        String type = (String) requestBody.get("type");
        
        // 参数校验
        if (roomId == null || roomId.isEmpty() || name == null || name.isEmpty() || description == null || description.isEmpty()) {
            return ResponseEntity.badRequest().body("房间ID、角色名称和角色描述不能为空");
        }
        
        try {
            // 调用服务层创建角色
            Characters character = charactersService.createCharacter(roomId, name, description, currentLocation, status, type);
            
            // 返回角色信息
            return ResponseEntity.status(HttpStatus.CREATED).body(Map.of(
                "id", character.getId(),
                "name", character.getName(),
                "description", character.getDescription(),
                "room_id", character.getRoomId(),
                "created_at", character.getCreatedAt()
            ));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("创建角色失败: " + e.getMessage());
        }
    }
    
    /**
     * 删除角色（可选）
     */
    @DeleteMapping("/{characterId}")
    public ResponseEntity<?> deleteCharacter(@PathVariable String characterId) {
        try {
            boolean success = charactersService.deleteCharacter(characterId);
            if (!success) {
                return ResponseEntity.notFound().build();
            }
            return ResponseEntity.ok(Map.of("status", "success"));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("删除角色失败: " + e.getMessage());
        }
    }
}