package com.example.chat_room_backend.service.impl;

import com.example.chat_room_backend.entity.Characters;
import com.example.chat_room_backend.entity.Rooms;
import com.example.chat_room_backend.mapper.CharactersMapper;
import com.example.chat_room_backend.mapper.ConversationsMapper;
import com.example.chat_room_backend.mapper.RoomsMapper;
import com.example.chat_room_backend.service.RoomsService;
import com.example.chat_room_backend.utils.CommonUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;

@Service
public class RoomsServiceImpl implements RoomsService {

    @Autowired
    private RoomsMapper roomsMapper;

    @Autowired
    private CharactersMapper charactersMapper;

    @Autowired
    private ConversationsMapper conversationsMapper;

    @Override
    public List<Rooms> getAllRooms() {
        return roomsMapper.selectAll();
    }

    @Override
    public Rooms getRoomById(String roomId) {
        return roomsMapper.selectById(roomId);
    }
    
    @Override
    public Rooms createRoom(String name, String worldview, String location, String creatorId) {
        // 创建房间
        Rooms room = new Rooms();
        room.setId(CommonUtils.generateUUID());
        room.setName(name);
        room.setWorldview(worldview);
        room.setLocation(location);
        room.setCreatorId(creatorId);
        room.setCreatedAt(CommonUtils.getCurrentTime());
        room.setUpdatedAt(CommonUtils.getCurrentTime());
        
        // 保存房间
        roomsMapper.insert(room);
        
        // 创建默认的AI管理员角色
        createDefaultCharacter(room.getId(), "AI管理员", "房间的AI管理员，负责分析剧情和推进剧情发展", "ai_admin");
        
        // 创建默认的旁白角色
        createDefaultCharacter(room.getId(), "旁白", "辅助推进剧情或进行环境描写", "narrator");
        
        return room;
    }
    
    @Override
    public boolean updateRoom(Rooms room) {
        room.setUpdatedAt(CommonUtils.getCurrentTime());
        return roomsMapper.update(room) > 0;
    }

    @Override
    @Transactional
    public boolean deleteRoom(String roomId) {
        // 先删除对话（因为对话引用了角色）
        conversationsMapper.deleteByRoomId(roomId);
        // 再删除角色（因为角色引用了房间）
        charactersMapper.deleteByRoomId(roomId);
        // 最后删除房间
        return roomsMapper.deleteById(roomId) > 0;
    }
    
    /**
     * 创建房间默认角色
     */
    private void createDefaultCharacter(String roomId, String name, String description, String type) {
        Characters character = new Characters();
        character.setId(CommonUtils.generateUUID());
        character.setName(name);
        character.setDescription(description);
        character.setRoomId(roomId);
        character.setType(type);
        character.setCreatedAt(CommonUtils.getCurrentTime());
        character.setUpdatedAt(CommonUtils.getCurrentTime());
        
        charactersMapper.insert(character);
    }
}