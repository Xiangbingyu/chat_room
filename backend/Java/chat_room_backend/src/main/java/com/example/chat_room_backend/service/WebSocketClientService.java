package com.example.chat_room_backend.service;

import com.example.chat_room_backend.entity.Conversations;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

import java.net.URI;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * WebSocket客户端服务，用于与Python后端建立连接
 */
@Service
public class WebSocketClientService {

    @Autowired
    private SimpMessagingTemplate messagingTemplate;

    @Autowired
    private ConversationsService conversationsService;

    // Python后端WebSocket地址
    @Value("${python.websocket.url:ws://localhost:8081/ws/ai}")
    private String pythonWebSocketUrl;

    // 存储WebSocket客户端连接
    private final Map<String, WebSocketClient> webSocketClients = new ConcurrentHashMap<>();

    /**
     * 连接到Python后端WebSocket服务
     */
    public void connectToPythonServer() {
        try {
            URI uri = new URI(pythonWebSocketUrl);
            WebSocketClient client = new WebSocketClient(uri) {
                @Override
                public void onOpen(ServerHandshake handshakedata) {
                    System.out.println("连接到Python后端WebSocket服务成功");
                }

                @Override
                public void onMessage(String message) {
                    System.out.println("收到Python后端消息: " + message);
                    // 处理AI回复，这里需要根据实际的消息格式进行解析
                    processAIResponse(message);
                }

                @Override
                public void onClose(int code, String reason, boolean remote) {
                    System.out.println("与Python后端WebSocket服务断开连接: " + reason);
                }

                @Override
                public void onError(Exception ex) {
                    System.err.println("WebSocket连接错误: " + ex.getMessage());
                }
            };

            // 连接WebSocket
            client.connect();
            // 存储客户端连接
            webSocketClients.put("python", client);
        } catch (Exception e) {
            System.err.println("连接到Python后端WebSocket服务失败: " + e.getMessage());
        }
    }

    /**
     * 发送消息到Python后端
     */
    public void sendMessageToPython(String message) {
        WebSocketClient client = webSocketClients.get("python");
        if (client != null && client.isOpen()) {
            client.send(message);
        } else {
            System.err.println("WebSocket连接未建立，无法发送消息");
        }
    }

    /**
     * 处理AI回复
     */
    private void processAIResponse(String message) {
        // 这里需要根据实际的消息格式进行解析
        // 假设消息格式为JSON，包含roomId、characterId、content等字段
        try {
            // 解析JSON消息，这里使用简单的字符串处理，实际项目中可以使用Jackson等库
            String roomId = extractValue(message, "roomId");
            String characterId = extractValue(message, "characterId");
            String content = extractValue(message, "content");
            String location = extractValue(message, "location");
            String status = extractValue(message, "status");
            String nextSpeaker = extractValue(message, "nextSpeaker");

            // 创建对话记录
            Conversations conversation = conversationsService.createOrUpdateConversation(
                    roomId, characterId, content, location, status, nextSpeaker
            );

            // 将AI回复推送给前端
            messagingTemplate.convertAndSend("/topic/chat/" + roomId, conversation);


            // 如果下一个说话者是AI角色，则触发AI调用逻辑
            if (isAICharacter(nextSpeaker)) {
                // 构造消息格式，发送给Python后端
                String newMessage = String.format("{\"roomId\":\"%s\",\"characterId\":\"%s\",\"content\":\"%s\",\"location\":\"%s\",\"status\":\"%s\",\"nextSpeaker\":\"%s\"}",
                        roomId, characterId, content, location, status, nextSpeaker);

                // 调用WebSocket客户端发送消息到Python后端
                sendMessageToPython(newMessage);
            }
        } catch (Exception e) {
            System.err.println("处理AI回复失败: " + e.getMessage());
        }
    }

    /**
     * 从JSON字符串中提取值（简单实现）
     */
    private String extractValue(String json, String key) {
        int startIndex = json.indexOf('"' + key + '"') + key.length() + 3;
        int endIndex = json.indexOf('"', startIndex);
        return json.substring(startIndex, endIndex);
    }

    /**
     * 判断是否是AI角色
     */
    private boolean isAICharacter(String characterId) {
        // 这里可以根据实际业务逻辑判断是否是AI角色
        // 例如，可以根据characterId的前缀或其他标识来判断
        return characterId != null && characterId.startsWith("ai_");
    }
}

