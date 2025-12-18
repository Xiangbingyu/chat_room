package com.example.chat_room_backend.utils;

import java.time.LocalDateTime;
import java.util.UUID;

public class CommonUtils {
    
    /**
     * 生成UUID字符串（不带连字符）
     */
    public static String generateUUID() {
        return UUID.randomUUID().toString().replace("-", "");
    }
    
    /**
     * 获取当前时间
     */
    public static LocalDateTime getCurrentTime() {
        return LocalDateTime.now();
    }
    
    /**
     * 判断字符串是否为空
     */
    public static boolean isEmpty(String str) {
        return str == null || str.trim().isEmpty();
    }
    
    /**
     * 判断字符串是否不为空
     */
    public static boolean isNotEmpty(String str) {
        return !isEmpty(str);
    }
}