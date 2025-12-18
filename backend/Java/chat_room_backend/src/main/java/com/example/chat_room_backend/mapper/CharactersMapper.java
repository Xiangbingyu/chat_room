package com.example.chat_room_backend.mapper;

import com.example.chat_room_backend.entity.Characters;
import java.util.List;
import java.util.Map;

public interface CharactersMapper {
    // 创建角色
    int insert(Characters character);
    
    // 根据房间ID查询所有角色
    List<Characters> selectByRoomId(String roomId);
    
    // 根据ID查询角色
    Characters selectById(String id);

    //根据ID查询角色名字
    String selectNameById(String id);

    // 更新角色信息
    int update(Characters character);
    
    // 删除角色
    int deleteById(String id);
    
    // 根据房间ID删除所有角色
    int deleteByRoomId(String roomId);
    
    // 根据角色类型查询
    Characters selectByTypeAndRoomId(Map<String, String> params);
}