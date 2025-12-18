package com.example.chat_room_backend.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;

/**
 * WebSocket配置类
 */
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        // 配置消息代理，设置消息前缀，客户端订阅地址以/topic开头
        config.enableSimpleBroker("/topic");
        // 配置应用程序目的地前缀，客户端发送消息地址以/app开头
        config.setApplicationDestinationPrefixes("/app");
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        // 注册WebSocket端点，客户端通过这个端点建立连接
        registry.addEndpoint("/ws/chat")
                .setAllowedOrigins("*") // 允许所有来源，生产环境应限制
                .withSockJS(); // 启用SockJS支持，提供降级方案
    }
}
