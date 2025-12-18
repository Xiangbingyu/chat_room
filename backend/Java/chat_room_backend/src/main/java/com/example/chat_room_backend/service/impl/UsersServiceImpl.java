package com.example.chat_room_backend.service.impl;

import com.example.chat_room_backend.entity.Users;
import com.example.chat_room_backend.mapper.UsersMapper;
import com.example.chat_room_backend.service.UsersService;
import com.example.chat_room_backend.utils.CommonUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Date;
import java.util.UUID;

@Service
public class UsersServiceImpl implements UsersService {
    @Autowired
    private UsersMapper usersMapper;

    @Override
    public Users register(String username, String password) {
        Users existingUser = usersMapper.selectByUsername(username);
        if (existingUser != null) {
            throw new RuntimeException("用户名已存在");
        }

        // 生成UUID作为用户ID
        String userId = UUID.randomUUID().toString();
        
        // 对密码进行加密
        String encryptedPassword = encryptPassword(password);
        
        // 创建用户对象
        Users user = new Users();
        user.setId(userId);
        user.setUsername(username);
        user.setPassword(encryptedPassword);
        user.setCreatedAt(CommonUtils.getCurrentTime());
        user.setUpdatedAt(CommonUtils.getCurrentTime());
        
        // 插入数据库
        usersMapper.insert(user);
        
        return user;
    }

    /**
     * 密码加密方法
     * @param password 原始密码
     * @return 加密后的密码
     */
    private String encryptPassword(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            md.update(password.getBytes());
            byte[] bytes = md.digest();
            StringBuilder sb = new StringBuilder();
            for (byte b : bytes) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("密码加密失败", e);
        }
    }
}