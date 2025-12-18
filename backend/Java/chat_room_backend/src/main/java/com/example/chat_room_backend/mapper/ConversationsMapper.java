package com.example.chat_room_backend.mapper;

import com.example.chat_room_backend.entity.Conversations;
import java.util.List;

public interface ConversationsMapper {
    // 创建/更新对话
    int insert(Conversations conversation);
    
    // 根据房间ID查询所有对话
    List<Conversations> selectByRoomId(String roomId);
    
    // 根据ID查询对话
    Conversations selectById(String id);
    
    // 更新对话信息
    int update(Conversations conversation);
    
    // 根据房间ID删除所有对话
    int deleteByRoomId(String roomId);
    
    // 检查角色是否参与了对话
    int countByCharacterId(String characterId);
}