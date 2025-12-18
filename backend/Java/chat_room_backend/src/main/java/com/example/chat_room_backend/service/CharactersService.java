package com.example.chat_room_backend.service;

import com.example.chat_room_backend.entity.Characters;
import java.util.List;

public interface CharactersService {
    // 获取房间内所有角色
    List<Characters> getCharactersByRoomId(String roomId);
    
    // 根据ID获取角色详情
    Characters getCharacterById(String characterId);
    
    // 创建角色
    Characters createCharacter(String roomId, String name, String description, String currentLocation, String status, String type);
    
    // 更新角色信息
    boolean updateCharacter(Characters character);
    
    // 删除角色
    boolean deleteCharacter(String characterId);
    
    // 根据类型和房间ID获取角色
    Characters getCharacterByTypeAndRoomId(String type, String roomId);
}