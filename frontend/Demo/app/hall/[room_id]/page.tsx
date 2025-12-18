'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useParams } from 'next/navigation';

interface Room {
  id: string;
  name: string;
  worldview: string;
  created_at: string;
}

interface Character {
  id: string;
  name: string;
  description: string;
  room_id: string;
  created_at: string;
}

export default function RoomDetail() {
  const params = useParams<{ room_id: string }>();
  const router = useRouter();
  const roomId = params.room_id;
  
  const [room, setRoom] = useState<Room | null>(null);
  const [characters, setCharacters] = useState<Character[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // 弹窗状态
  const [isAddCharacterModalOpen, setIsAddCharacterModalOpen] = useState(false);
  
  // 添加角色表单
  const [characterForm, setCharacterForm] = useState({
    name: '',
    description: ''
  });
  
  // 表单错误
  const [formErrors, setFormErrors] = useState<{ name?: string; description?: string }>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [addingCharacter, setAddingCharacter] = useState(false);

  // 获取房间信息
  useEffect(() => {
    const fetchRoomInfo = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // 获取房间列表，然后根据room_id过滤
        const roomsResponse = await fetch('/api/db/rooms');
        if (!roomsResponse.ok) {
          throw new Error('获取房间信息失败');
        }
        
        const roomsData = await roomsResponse.json();
        const currentRoom = roomsData.data.find((r: Room) => r.id === roomId);
        
        if (!currentRoom) {
          throw new Error('房间不存在');
        }
        
        setRoom(currentRoom);
        
        // 获取角色列表
        const charactersResponse = await fetch(`/api/db/rooms/${roomId}/characters`);
        if (!charactersResponse.ok) {
          throw new Error('获取角色列表失败');
        }
        
        const charactersData = await charactersResponse.json();
        setCharacters(charactersData.data);
        
      } catch (error) {
        setError(error instanceof Error ? error.message : '获取房间信息失败');
      } finally {
        setLoading(false);
      }
    };
    
    if (roomId) {
      fetchRoomInfo();
    }
  }, [roomId]);

  // 表单输入处理
  const handleCharacterInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setCharacterForm(prev => ({ ...prev, [name]: value }));
    // 清除该字段的错误提示
    if (formErrors[name as keyof typeof formErrors]) {
      setFormErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  // 表单验证
  const validateCharacterForm = () => {
    const newErrors: { name?: string; description?: string } = {};
    
    if (!characterForm.name.trim()) {
      newErrors.name = '角色名不能为空';
    } else if (characterForm.name.trim().length < 2) {
      newErrors.name = '角色名至少需要2个字符';
    } else if (characterForm.name.trim().length > 30) {
      newErrors.name = '角色名不能超过30个字符';
    }
    
    if (!characterForm.description.trim()) {
      newErrors.description = '角色描述不能为空';
    } else if (characterForm.description.trim().length < 5) {
      newErrors.description = '角色描述至少需要5个字符';
    } else if (characterForm.description.trim().length > 500) {
      newErrors.description = '角色描述不能超过500个字符';
    }
    
    setFormErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 添加角色
  const handleAddCharacter = async () => {
    if (!validateCharacterForm()) {
      return;
    }
    
    setAddingCharacter(true);
    setSubmitError(null);
    
    try {
      const response = await fetch('/api/db/characters', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: characterForm.name.trim(),
          description: characterForm.description.trim(),
          room_id: roomId
        })
      });
      
      if (!response.ok) {
        throw new Error('添加角色失败');
      }
      
      const result = await response.json();
      
      // 更新角色列表
      setCharacters(prev => [...prev, result.data]);
      
      // 关闭弹窗并重置表单
      setIsAddCharacterModalOpen(false);
      setCharacterForm({ name: '', description: '' });
      setFormErrors({});
      
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : '添加角色失败，请重试');
    } finally {
      setAddingCharacter(false);
    }
  };

  // 进入房间
  const handleEnterChatRoom = () => {
    router.push(`/hall/${roomId}/chat_room`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background p-4 sm:p-6 lg:p-8 flex items-center justify-center">
        <div className="text-foreground">加载中...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background p-4 sm:p-6 lg:p-8 flex items-center justify-center">
        <div className="text-red-500 dark:text-red-400">{error}</div>
      </div>
    );
  }

  if (!room) {
    return (
      <div className="min-h-screen bg-background p-4 sm:p-6 lg:p-8 flex items-center justify-center">
        <div className="text-foreground">房间不存在</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background p-4 sm:p-6 lg:p-8">
      <div className="max-w-4xl mx-auto">
        {/* 返回按钮 */}
        <div className="mb-6">
          <Link
            href="/hall"
            className="inline-flex items-center text-sm font-medium text-foreground hover:underline"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            返回大厅
          </Link>
        </div>

        {/* 房间信息 */}
        <div className="bg-white dark:bg-zinc-800 rounded-xl shadow-sm p-6 mb-8">
          <h1 className="text-3xl font-bold mb-2 text-foreground">{room.name}</h1>
          <div className="text-zinc-600 dark:text-zinc-400 whitespace-pre-line">{room.worldview}</div>
        </div>

        {/* 角色列表 */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold text-foreground">角色列表</h2>
            <button
              onClick={() => setIsAddCharacterModalOpen(true)}
              className="inline-flex items-center justify-center h-10 px-4 rounded-lg bg-foreground text-background font-medium transition-colors hover:bg-zinc-800 dark:hover:bg-zinc-300 dark:hover:text-zinc-900"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              添加角色
            </button>
          </div>

          {characters.length === 0 ? (
            <div className="bg-white dark:bg-zinc-800 rounded-xl shadow-sm p-8 text-center">
              <p className="text-zinc-500 dark:text-zinc-400 mb-4">暂无角色，点击上方按钮添加角色</p>
              <p className="text-xs text-zinc-400 dark:text-zinc-500">至少需要4个角色才能进入房间</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {characters.map((character) => (
                <div key={character.id} className="bg-white dark:bg-zinc-800 rounded-xl shadow-sm p-5">
                  <h3 className="text-lg font-semibold mb-2 text-foreground">{character.name}</h3>
                  <p className="text-zinc-600 dark:text-zinc-400 text-sm whitespace-pre-line">{character.description}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 进入房间按钮 */}
        {characters.length > 3 && (
          <div className="flex justify-center">
            <button
              onClick={handleEnterChatRoom}
              className="inline-flex items-center justify-center h-12 px-8 rounded-lg bg-foreground text-background font-medium transition-colors hover:bg-zinc-800 dark:hover:bg-zinc-300 dark:hover:text-zinc-900 text-lg"
            >
              进入房间
              <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
          </div>
        )}
      </div>

      {/* 添加角色弹窗 */}
      {isAddCharacterModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-zinc-800 rounded-xl shadow-lg max-w-md w-full">
            {/* 弹窗头部 */}
            <div className="p-6 border-b border-zinc-200 dark:border-zinc-700">
              <h2 className="text-xl font-bold text-foreground">添加角色</h2>
            </div>
            
            {/* 弹窗内容 */}
            <div className="p-6">
              {/* 错误提示 */}
              {submitError && (
                <div className="bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 p-3 rounded-lg mb-4">
                  {submitError}
                </div>
              )}
              
              {/* 角色名 */}
              <div className="mb-5">
                <label htmlFor="characterName" className="block text-sm font-medium text-foreground mb-1">
                  角色名
                </label>
                <input
                  type="text"
                  id="characterName"
                  name="name"
                  value={characterForm.name}
                  onChange={handleCharacterInputChange}
                  placeholder="请输入角色名称"
                  className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-foreground transition-all ${formErrors.name ? 'border-red-500 dark:border-red-500' : 'border-zinc-300 dark:border-zinc-600 dark:bg-zinc-700 dark:text-white'}`}
                  disabled={addingCharacter}
                />
                {formErrors.name && (
                  <p className="text-red-500 text-xs dark:text-red-400 mt-1">{formErrors.name}</p>
                )}
              </div>

              {/* 角色描述 */}
              <div className="mb-6">
                <label htmlFor="characterDescription" className="block text-sm font-medium text-foreground mb-1">
                  角色描述
                </label>
                <textarea
                  id="characterDescription"
                  name="description"
                  value={characterForm.description}
                  onChange={handleCharacterInputChange}
                  placeholder="请输入角色描述..."
                  rows={4}
                  className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-foreground transition-all resize-none ${formErrors.description ? 'border-red-500 dark:border-red-500' : 'border-zinc-300 dark:border-zinc-600 dark:bg-zinc-700 dark:text-white'}`}
                  disabled={addingCharacter}
                />
                <div className="flex justify-between items-center mt-1">
                  {formErrors.description && (
                    <p className="text-red-500 text-xs dark:text-red-400">{formErrors.description}</p>
                  )}
                  <p className="text-zinc-500 text-xs dark:text-zinc-400">
                    {characterForm.description.length}/500
                  </p>
                </div>
              </div>
            </div>

            {/* 弹窗底部 */}
            <div className="p-6 border-t border-zinc-200 dark:border-zinc-700 flex justify-end gap-3">
              <button
                onClick={() => {
                  setIsAddCharacterModalOpen(false);
                  setCharacterForm({ name: '', description: '' });
                  setFormErrors({});
                  setSubmitError(null);
                }}
                className="inline-flex items-center justify-center h-10 px-4 rounded-lg border border-zinc-300 text-zinc-700 font-medium transition-colors hover:bg-zinc-100 dark:border-zinc-600 dark:text-zinc-300 dark:hover:bg-zinc-700"
                disabled={addingCharacter}
              >
                取消
              </button>
              <button
                onClick={handleAddCharacter}
                className="inline-flex items-center justify-center h-10 px-4 rounded-lg bg-foreground text-background font-medium transition-colors hover:bg-zinc-800 dark:hover:bg-zinc-300 dark:hover:text-zinc-900"
                disabled={addingCharacter}
              >
                {addingCharacter ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white dark:border-black mx-auto"></div>
                ) : (
                  '创建'
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}