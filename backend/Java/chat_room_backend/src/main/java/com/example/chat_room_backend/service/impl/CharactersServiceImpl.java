package com.example.chat_room_backend.service.impl;

import com.example.chat_room_backend.entity.Characters;
import com.example.chat_room_backend.mapper.CharactersMapper;
import com.example.chat_room_backend.mapper.ConversationsMapper;
import com.example.chat_room_backend.service.CharactersService;
import com.example.chat_room_backend.utils.CommonUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

@Service
public class CharactersServiceImpl implements CharactersService {
    
    @Autowired
    private CharactersMapper charactersMapper;
    
    @Autowired
    private ConversationsMapper conversationsMapper;
    
    @Override
    public List<Characters> getCharactersByRoomId(String roomId) {
        return charactersMapper.selectByRoomId(roomId);
    }
    
    @Override
    public Characters getCharacterById(String characterId) {
        return charactersMapper.selectById(characterId);
    }
    
    @Override
    public Characters createCharacter(String roomId, String name, String description, String currentLocation, String status, String type) {
        // 创建角色
        Characters character = new Characters();
        character.setId(CommonUtils.generateUUID());
        character.setName(name);
        character.setDescription(description);
        character.setRoomId(roomId);
        character.setCurrentLocation(currentLocation);
        character.setStatus(status);
        character.setType(CommonUtils.isEmpty(type) ? "user" : type); // 默认角色类型为user
        character.setCreatedAt(CommonUtils.getCurrentTime());
        character.setUpdatedAt(CommonUtils.getCurrentTime());
        
        // 保存角色
        charactersMapper.insert(character);
        return character;
    }
    
    @Override
    public boolean updateCharacter(Characters character) {
        character.setUpdatedAt(CommonUtils.getCurrentTime());
        return charactersMapper.update(character) > 0;
    }
    
    @Override
    public boolean deleteCharacter(String characterId) {
        // 检查角色是否参与了对话
        int conversationCount = conversationsMapper.countByCharacterId(characterId);
        if (conversationCount > 0) {
            // 角色参与了对话，不允许删除
            throw new RuntimeException("该角色已参与对话，无法删除");
        }
        // 角色未参与对话，可以删除
        return charactersMapper.deleteById(characterId) > 0;
    }
    
    @Override
    public Characters getCharacterByTypeAndRoomId(String type, String roomId) {
        Map<String, String> params = new HashMap<>();
        params.put("type", type);
        params.put("roomId", roomId);
        return charactersMapper.selectByTypeAndRoomId(params);
    }
}