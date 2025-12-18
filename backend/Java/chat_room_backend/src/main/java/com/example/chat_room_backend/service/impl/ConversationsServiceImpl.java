package com.example.chat_room_backend.service.impl;

import com.example.chat_room_backend.entity.Conversations;
import com.example.chat_room_backend.mapper.CharactersMapper;
import com.example.chat_room_backend.mapper.ConversationsMapper;
import com.example.chat_room_backend.service.ConversationsService;
import com.example.chat_room_backend.service.WebSocketClientService;
import com.example.chat_room_backend.utils.CommonUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ConversationsServiceImpl implements ConversationsService {

    @Autowired
    private ConversationsMapper conversationsMapper;

    @Autowired
    private CharactersMapper charactersMapper;
    

    @Override
    public List<Conversations> getConversationsByRoomId(String roomId) {
        return conversationsMapper.selectByRoomId(roomId);
    }

    @Override
    public Conversations getConversationById(String conversationId) {
        return conversationsMapper.selectById(conversationId);
    }

    @Override
    public Conversations createOrUpdateConversation(String roomId, String characterId, String content, String currentLocation, String status, String nextSpeaker) {
        // 创建新对话
        Conversations conversation = new Conversations();
        conversation.setId(CommonUtils.generateUUID());
        conversation.setRoomId(roomId);
        conversation.setCharacterId(characterId);
        conversation.setContent(content);
        conversation.setCurrentLocation(currentLocation);
        conversation.setStatus(status);
        conversation.setNextSpeaker(nextSpeaker);
        conversation.setCreatedAt(CommonUtils.getCurrentTime());
        conversation.setUpdatedAt(CommonUtils.getCurrentTime());

        // 保存对话
        conversationsMapper.insert(conversation);

        //获取角色名字
        String name = charactersMapper.selectNameById(conversation.getCharacterId());
        conversation.setCharacterName(name);
        

        
        return conversation;
    }
    


    @Override
    public boolean updateConversation(Conversations conversation) {
        conversation.setUpdatedAt(CommonUtils.getCurrentTime());
        return conversationsMapper.update(conversation) > 0;
    }
}