package com.example.chat_room_backend.mapper;

import com.example.chat_room_backend.entity.Rooms;
import java.util.List;

public interface RoomsMapper {
    // 创建房间
    int insert(Rooms room);
    
    // 查询所有房间
    List<Rooms> selectAll();
    
    // 根据ID查询房间
    Rooms selectById(String id);
    
    // 更新房间信息
    int update(Rooms room);
    
    // 删除房间
    int deleteById(String id);
}