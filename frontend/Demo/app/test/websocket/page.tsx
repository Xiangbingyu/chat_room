'use client';

import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

export default function WebSocketTestPage() {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<string[]>([]);
  const [testResult, setTestResult] = useState<string>('');

  // 连接到WebSocket服务器
  useEffect(() => {
    const newSocket = io('http://localhost:5000');

    newSocket.on('connect', () => {
      setIsConnected(true);
      addMessage('已连接到服务器');
    });

    newSocket.on('disconnect', () => {
      setIsConnected(false);
      addMessage('与服务器断开连接');
    });

    newSocket.on('connection_response', (data) => {
      addMessage(`连接响应: ${JSON.stringify(data)}`);
    });

    newSocket.on('room_controller_response', (data) => {
      addMessage(`房间控制器响应: ${JSON.stringify(data)}`);
      setTestResult('房间控制器测试成功');
    });

    newSocket.on('character_controller_response', (data) => {
      addMessage(`人物控制器响应: ${JSON.stringify(data)}`);
      setTestResult('人物控制器测试成功');
    });

    setSocket(newSocket);

    return () => {
      newSocket.disconnect();
    };
  }, []);

  const addMessage = (message: string) => {
    setMessages((prev) => [...prev, message]);
  };

  // 测试房间控制器
  const testRoomController = () => {
    if (!socket || !isConnected) {
      addMessage('请先连接到服务器');
      return;
    }

    const testData = {
      history_messages: [
        { role: '用户', content: '你好，欢迎来到AI聊天室！' },
        { role: '系统', content: '很高兴为您服务！' }
      ],
      world_background: '这是一个未来科技世界，人类与AI和谐共处',
      character_settings: [
        {
          name: '小明',
          background: '一名年轻的AI工程师，对新技术充满热情'
        },
        {
          name: '小红',
          background: '一位经验丰富的AI助手，擅长解决各种问题'
        }
      ]
    };

    addMessage(`发送房间控制器测试数据: ${JSON.stringify(testData)}`);
    socket.emit('room_controller', testData);
  };

  // 测试人物控制器
  const testCharacterController = () => {
    if (!socket || !isConnected) {
      addMessage('请先连接到服务器');
      return;
    }

    const testData = {
      history_messages: [
        { role: '用户', content: '你好，欢迎来到AI聊天室！' },
        { role: '系统', content: '很高兴为您服务！' }
      ],
      world_background: '这是一个未来科技世界，人类与AI和谐共处',
      character_settings: [
        {
          name: '小明',
          background: '一名年轻的AI工程师，对新技术充满热情'
        },
        {
          name: '小红',
          background: '一位经验丰富的AI助手，擅长解决各种问题'
        }
      ],
      character_name: '小明'
    };

    addMessage(`发送人物控制器测试数据: ${JSON.stringify(testData)}`);
    socket.emit('character_controller', testData);
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">WebSocket测试页面</h1>
      
      <div className="mb-4">
        <p className={`inline-block px-3 py-1 rounded-full ${isConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          连接状态: {isConnected ? '已连接' : '未连接'}
        </p>
      </div>

      <div className="flex gap-4 mb-4">
        <button 
          onClick={testRoomController}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          测试房间控制器
        </button>
        <button 
          onClick={testCharacterController}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          测试人物控制器
        </button>
      </div>

      {testResult && (
        <div className="mb-4 p-3 bg-yellow-100 text-yellow-800 rounded">
          {testResult}
        </div>
      )}

      <div className="border border-gray-300 rounded p-4 h-96 overflow-y-auto">
        <h2 className="text-lg font-semibold mb-2">消息记录</h2>
        <div className="space-y-2">
          {messages.map((message, index) => (
            <div key={index} className="p-2 bg-gray-100 rounded">
              {message}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}