'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';

// 定义对话记录的类型
interface Conversation {
  id: string;
  room_id: string;
  character_id: string;
  character_name: string;
  content: string;
  created_at: string;
}

// 定义角色的类型
interface Character {
  id: string;
  name: string;
  description: string;
  room_id: string;
  created_at: string;
}

export default function ChatRoom() {
  const { room_id } = useParams<{ room_id: string }>();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [characters, setCharacters] = useState<Character[]>([]);
  const [narratorId, setNarratorId] = useState<string | null>(null);
  const [messageInput, setMessageInput] = useState<string>('');
  const [sending, setSending] = useState<boolean>(false);

  // 获取对话记录
  useEffect(() => {
    const fetchConversations = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch(`/api/db/rooms/${room_id}/conversations`);
        
        if (!response.ok) {
          throw new Error('获取对话记录失败');
        }
        
        const result = await response.json();
        setConversations(result.data || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : '获取对话记录失败，请重试');
      } finally {
        setLoading(false);
      }
    };

    if (room_id) {
      fetchConversations();
    }
  }, [room_id]);

  // 获取角色列表，找到旁白角色ID
  useEffect(() => {
    const fetchCharacters = async () => {
      try {
        const response = await fetch(`/api/db/rooms/${room_id}/characters`);
        
        if (!response.ok) {
          throw new Error('获取角色列表失败');
        }
        
        const result = await response.json();
        setCharacters(result.data || []);
        
        // 找到旁白角色的ID
        const narrator = result.data.find((char: Character) => char.name === '旁白');
        if (narrator) {
          setNarratorId(narrator.id);
        }
      } catch (err) {
        console.error('获取角色列表失败:', err);
      }
    };

    if (room_id) {
      fetchCharacters();
    }
  }, [room_id]);

  // 发送消息
  const handleSendMessage = async () => {
    if (!messageInput.trim() || !narratorId || !room_id) {
      return;
    }

    try {
      setSending(true);
      
      const response = await fetch('/api/db/conversations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          room_id,
          character_id: narratorId,
          content: messageInput.trim()
        })
      });
      
      if (!response.ok) {
        throw new Error('发送消息失败');
      }
      
      const result = await response.json();
      
      // 添加新消息到对话列表
      setConversations(prev => [...prev, result.data]);
      
      // 清空输入框
      setMessageInput('');
    } catch (err) {
      alert(err instanceof Error ? err.message : '发送消息失败，请重试');
    } finally {
      setSending(false);
    }
  };

  // 处理按键事件，Enter键发送消息
  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 页面标题 */}
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">聊天记录</h1>

        {/* 加载状态 */}
        {loading && (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 dark:border-blue-400"></div>
          </div>
        )}

        {/* 错误提示 */}
        {error && (
          <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-200 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {/* 对话记录列表 */}
        {!loading && !error && (
          <div className="space-y-6">
            {conversations.length > 0 ? (
              conversations.map((conversation) => (
                <div key={conversation.id} className="flex items-start">
                  {/* 角色信息 */}
                  <div className="flex-shrink-0 w-16 h-16 rounded-full bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center mr-4">
                    <span className="text-blue-600 dark:text-blue-400 font-semibold text-sm">
                      {conversation.character_name.charAt(0)}
                    </span>
                  </div>
                  
                  {/* 对话内容 */}
                  <div className="flex-1">
                    <div className="flex items-center mb-1">
                      <h3 className="font-semibold text-gray-900 dark:text-white">
                        {conversation.character_name}
                      </h3>
                      <span className="text-xs text-gray-500 dark:text-gray-400 ml-3">
                        {new Date(conversation.created_at).toLocaleString()}
                      </span>
                    </div>
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm dark:shadow-gray-700/50">
                      <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                        {conversation.content}
                      </p>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="flex items-start">
                {/* 角色信息 - 旁白 */}
                <div className="flex-shrink-0 w-16 h-16 rounded-full bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center mr-4">
                  <span className="text-blue-600 dark:text-blue-400 font-semibold text-sm">
                    旁
                  </span>
                </div>
                
                {/* 输入气泡 */}
                <div className="flex-1">
                  <div className="flex items-center mb-1">
                    <h3 className="font-semibold text-gray-900 dark:text-white">旁白</h3>
                    <span className="text-xs text-gray-500 dark:text-gray-400 ml-3">开场白</span>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm dark:shadow-gray-700/50">
                    <textarea
                      value={messageInput}
                      onChange={(e) => setMessageInput(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="输入开场白..."
                      className="w-full border-none resize-none focus:outline-none bg-transparent text-gray-700 dark:text-gray-300 min-h-[80px]"
                    />
                  </div>
                  <div className="mt-2 flex justify-end">
                    <button
                      onClick={handleSendMessage}
                      disabled={sending || !messageInput.trim()}
                      className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg disabled:bg-blue-300 disabled:cursor-not-allowed transition-colors"
                    >
                      {sending ? '发送中...' : '发送'}
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}