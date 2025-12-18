package com.example.chat_room_backend.controller;

import com.example.chat_room_backend.entity.Rooms;
import com.example.chat_room_backend.service.RoomsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import tools.jackson.databind.ObjectMapper;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/rooms")
public class RoomsController {
    
    @Autowired
    private RoomsService roomsService;

    @Autowired
    private ObjectMapper objectMapper;
    
    /**
     * 获取所有房间列表
     */
    @GetMapping
    public ResponseEntity<?> getAllRooms() {
        try {
            List<Rooms> rooms = roomsService.getAllRooms();
            return ResponseEntity.ok(rooms);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("获取房间列表失败: " + e.getMessage());
        }
    }
    
    /**
     * 获取单个房间详情
     */
    @GetMapping("/{roomId}")
    public ResponseEntity<?> getRoomById(@PathVariable String roomId) {
        try {
            Rooms room = roomsService.getRoomById(roomId);
            if (room == null) {
                return ResponseEntity.notFound().build();
            }
            return ResponseEntity.ok(room);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("获取房间详情失败: " + e.getMessage());
        }
    }
    
    /**
     * 创建房间
     */
    @PostMapping
    public ResponseEntity<?> createRoom(@RequestBody Map<String, Object> requestBody) {
        String name = (String) requestBody.get("name");
        String worldview = (String) requestBody.get("worldview");
        List<String> location = (List<String>) requestBody.get("location");
        // 同时支持creator_id和creatorId两种命名方式
        String creatorId = (String) requestBody.get("creator_id");
        if (creatorId == null) {
            creatorId = (String) requestBody.get("creatorId");
        }
        
        // 参数校验
        if (name == null || name.isEmpty() || worldview == null || worldview.isEmpty() || creatorId == null || creatorId.isEmpty()) {
            return ResponseEntity.badRequest().body("房间名称、世界观描述和创建者ID不能为空");
        }
        
        try {
            // 调用服务层创建房间
            // 将 List<String> location 转为json格式
            String locationJsonStr = objectMapper.writeValueAsString(location);
            //todo : 登录检验： 利用拦截器获取用户id
            Rooms room = roomsService.createRoom(name, worldview, locationJsonStr, creatorId);
            
            // 返回房间信息
            return ResponseEntity.status(HttpStatus.CREATED).body(Map.of(
                "id", room.getId()
            ));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("创建房间失败: " + e.getMessage());
        }
    }
    
    /**
     * 删除房间（可选）
     */
    @DeleteMapping("/{roomId}")
    public ResponseEntity<?> deleteRoom(@PathVariable String roomId) {
        try {
            boolean success = roomsService.deleteRoom(roomId);
            if (!success) {
                return ResponseEntity.notFound().build();
            }
            return ResponseEntity.ok(Map.of("status", "success"));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("删除房间失败: " + e.getMessage());
        }
    }
}