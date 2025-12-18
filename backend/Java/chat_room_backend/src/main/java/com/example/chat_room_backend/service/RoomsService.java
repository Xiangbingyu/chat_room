package com.example.chat_room_backend.service;

import com.example.chat_room_backend.entity.Rooms;
import java.util.List;

public interface RoomsService {
    // 获取所有房间列表
    List<Rooms> getAllRooms();
    
    // 根据ID获取房间详情
    Rooms getRoomById(String roomId);
    
    // 创建房间
    Rooms createRoom(String name, String worldview, String location, String creatorId);
    
    // 更新房间信息
    boolean updateRoom(Rooms room);
    
    // 删除房间
    boolean deleteRoom(String roomId);
}