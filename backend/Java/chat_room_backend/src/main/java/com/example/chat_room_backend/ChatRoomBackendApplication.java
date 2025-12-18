package com.example.chat_room_backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.transaction.annotation.EnableTransactionManagement;
import org.springframework.transaction.annotation.Transactional;

@SpringBootApplication
@MapperScan("com.example.chat_room_backend.mapper") // 扫描Mapper接口
@EnableTransactionManagement //开启注解方式的事务管理
public class ChatRoomBackendApplication {

    public static void main(String[] args) {
        SpringApplication.run(ChatRoomBackendApplication.class, args);
    }

}
