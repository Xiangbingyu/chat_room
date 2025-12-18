package com.example.chat_room_backend.listener;

import com.example.chat_room_backend.service.WebSocketClientService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

/**
 * 应用启动监听器，用于在应用启动时连接到Python后端WebSocket服务
 */
@Component
public class WebSocketStartupListener implements ApplicationRunner {

    @Autowired
    private WebSocketClientService webSocketClientService;

    @Override
    public void run(ApplicationArguments args) throws Exception {
        // 应用启动后连接到Python后端WebSocket服务
        webSocketClientService.connectToPythonServer();
    }
}
