'use client';

import { useState, useEffect } from 'react';

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

export default function DbTestPage() {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [characters, setCharacters] = useState<Character[]>([]);
  const [newRoom, setNewRoom] = useState({ name: '', worldview: '' });
  const [newCharacter, setNewCharacter] = useState({ name: '', description: '', room_id: '' });
  const [selectedRoom, setSelectedRoom] = useState<string>('');
  const [message, setMessage] = useState<string>('');

  // 获取所有房间
  const fetchRooms = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/db/rooms');
      const data = await response.json();
      if (data.status === 'success') {
        setRooms(data.data);
        setMessage('获取房间成功');
      } else {
        setMessage(`获取房间失败: ${data.message}`);
      }
    } catch (error) {
      setMessage(`获取房间失败: ${error instanceof Error ? error.message : '未知错误'}`);
    }
  };

  // 根据房间ID获取角色
  const fetchCharactersByRoom = async (roomId: string) => {
    try {
      const response = await fetch(`http://localhost:5000/api/db/rooms/${roomId}/characters`);
      const data = await response.json();
      if (data.status === 'success') {
        setCharacters(data.data);
        setMessage('获取角色成功');
      } else {
        setMessage(`获取角色失败: ${data.message}`);
      }
    } catch (error) {
      setMessage(`获取角色失败: ${error instanceof Error ? error.message : '未知错误'}`);
    }
  };

  // 创建房间
  const createRoom = async () => {
    if (!newRoom.name || !newRoom.worldview) {
      setMessage('请填写房间名称和世界观');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/db/rooms', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newRoom),
      });
      const data = await response.json();
      if (data.status === 'success') {
        fetchRooms();
        setNewRoom({ name: '', worldview: '' });
        setMessage('创建房间成功');
      } else {
        setMessage(`创建房间失败: ${data.message}`);
      }
    } catch (error) {
      setMessage(`创建房间失败: ${error instanceof Error ? error.message : '未知错误'}`);
    }
  };

  // 创建角色
  const createCharacter = async () => {
    if (!newCharacter.name || !newCharacter.description || !newCharacter.room_id) {
      setMessage('请填写角色名称、描述和所属房间');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/db/characters', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newCharacter),
      });
      const data = await response.json();
      if (data.status === 'success') {
        if (selectedRoom) {
          fetchCharactersByRoom(selectedRoom);
        }
        setNewCharacter({ name: '', description: '', room_id: '' });
        setMessage('创建角色成功');
      } else {
        setMessage(`创建角色失败: ${data.message}`);
      }
    } catch (error) {
      setMessage(`创建角色失败: ${error instanceof Error ? error.message : '未知错误'}`);
    }
  };

  // 当选择房间变化时获取角色
  useEffect(() => {
    if (selectedRoom) {
      fetchCharactersByRoom(selectedRoom);
    }
  }, [selectedRoom]);

  // 初始加载房间
  useEffect(() => {
    fetchRooms();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">数据库接口测试</h1>
      
      {message && (
        <div className="mb-4 p-2 bg-blue-100 text-blue-800 rounded">
          {message}
        </div>
      )}

      {/* 创建房间 */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-2">创建房间</h2>
        <div className="flex flex-col gap-2">
          <input
            type="text"
            placeholder="房间名称"
            value={newRoom.name}
            onChange={(e) => setNewRoom({ ...newRoom, name: e.target.value })}
            className="border p-2 rounded"
          />
          <textarea
            placeholder="房间世界观"
            value={newRoom.worldview}
            onChange={(e) => setNewRoom({ ...newRoom, worldview: e.target.value })}
            className="border p-2 rounded"
            rows={3}
          />
          <button
            onClick={createRoom}
            className="bg-green-500 text-white p-2 rounded hover:bg-green-600"
          >
            创建房间
          </button>
        </div>
      </div>

      {/* 房间列表 */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-2">房间列表</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {rooms.map((room) => (
            <div
              key={room.id}
              className={`border p-4 rounded cursor-pointer ${selectedRoom === room.id ? 'border-blue-500 bg-blue-50' : 'hover:bg-gray-50'}`}
              onClick={() => setSelectedRoom(room.id)}
            >
              <h3 className="font-bold">{room.name}</h3>
              <p className="text-sm text-gray-600">{room.worldview}</p>
              <p className="text-xs text-gray-500 mt-2">创建时间: {new Date(room.created_at).toLocaleString()}</p>
            </div>
          ))}
        </div>
      </div>

      {/* 创建角色 */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-2">创建角色</h2>
        <div className="flex flex-col gap-2">
          <input
            type="text"
            placeholder="角色名称"
            value={newCharacter.name}
            onChange={(e) => setNewCharacter({ ...newCharacter, name: e.target.value })}
            className="border p-2 rounded"
          />
          <textarea
            placeholder="角色描述"
            value={newCharacter.description}
            onChange={(e) => setNewCharacter({ ...newCharacter, description: e.target.value })}
            className="border p-2 rounded"
            rows={3}
          />
          <select
            value={newCharacter.room_id}
            onChange={(e) => setNewCharacter({ ...newCharacter, room_id: e.target.value })}
            className="border p-2 rounded"
          >
            <option value="">选择所属房间</option>
            {rooms.map((room) => (
              <option key={room.id} value={room.id}>
                {room.name}
              </option>
            ))}
          </select>
          <button
            onClick={createCharacter}
            className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
          >
            创建角色
          </button>
        </div>
      </div>

      {/* 角色列表 */}
      {selectedRoom && (
        <div>
          <h2 className="text-xl font-semibold mb-2">角色列表</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {characters.map((character) => (
              <div key={character.id} className="border p-4 rounded">
                <h3 className="font-bold">{character.name}</h3>
                <p className="text-sm text-gray-600">{character.description}</p>
                <p className="text-xs text-gray-500 mt-2">创建时间: {new Date(character.created_at).toLocaleString()}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}