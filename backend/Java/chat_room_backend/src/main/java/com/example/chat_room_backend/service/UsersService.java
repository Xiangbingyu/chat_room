package com.example.chat_room_backend.service;


import com.example.chat_room_backend.entity.Users;

public interface UsersService {
    /**
     * 用户注册
     * @param username 用户名
     * @param password 密码
     * @return 创建的用户对象
     */
    Users register(String username, String password);
}