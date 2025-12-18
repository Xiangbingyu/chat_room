package com.example.chat_room_backend.controller;


import com.example.chat_room_backend.entity.Users;
import com.example.chat_room_backend.service.UsersService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/users")
public class UsersController {
    @Autowired
    private UsersService usersService;

    @PostMapping
    public ResponseEntity<?> register(@RequestBody Map<String, String> requestBody) {
        try {
            // 获取请求参数
            String username = requestBody.get("username");
            String password = requestBody.get("password");
            
            // 参数验证
            if (username == null || username.isEmpty() || password == null || password.isEmpty()) {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("用户名和密码不能为空");
            }
            
            // 调用服务层进行注册
            Users user = usersService.register(username, password);
            
            // 构建返回结果
            return ResponseEntity.status(HttpStatus.CREATED).body(Map.of(
                "id", user.getId(),
                "username", user.getUsername(),
                "created_at", user.getCreatedAt()
            ));
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(e.getMessage());
        }
    }
}