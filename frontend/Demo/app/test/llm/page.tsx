'use client';

import { useState } from 'react';

export default function LLMTestPage() {
  const [messages, setMessages] = useState<string[]>([]);
  const [testResult, setTestResult] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  const addMessage = (message: string) => {
    setMessages((prev) => [...prev, message]);
  };

  // 测试房间控制器API
  const testRoomController = async () => {
    setIsLoading(true);
    setTestResult('');

    const testData = {
      history_messages: [
        "你好，我是小明，很高兴认识你！",
        "你好小明，我是小红，最近在研究什么新的AI技术吗？"
      ],
      world_background: '这是一个未来科技世界，人类与AI和谐共处，科技高度发达但保持着人文关怀',
      character_settings: [
        '小明: 一名年轻的AI工程师，对新技术充满热情，性格开朗乐观',
        '小红: 一位经验丰富的AI伦理学家，关注科技发展对社会的影响'
      ]
    };

    addMessage(`发送房间控制器测试数据: ${JSON.stringify(testData)}`);

    try {
      const response = await fetch('http://localhost:5000/api/llm/room_controller', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(testData),
      });

      const data = await response.json();
      addMessage(`房间控制器响应: ${JSON.stringify(data)}`);
      setTestResult('房间控制器测试成功');
    } catch (error) {
      addMessage(`测试失败: ${error instanceof Error ? error.message : String(error)}`);
      setTestResult('房间控制器测试失败');
    } finally {
      setIsLoading(false);
    }
  };

  // 测试人物控制器API
  const testCharacterController = async () => {
    setIsLoading(true);
    setTestResult('');

    const testData = {
      history_messages: [
        "你好，我是小明，很高兴认识你！",
        "你好小明，我是小红，最近在研究什么新的AI技术吗？"
      ],
      world_background: '这是一个未来科技世界，人类与AI和谐共处，科技高度发达但保持着人文关怀',
      character_settings: [
        '小明: 一名年轻的AI工程师，对新技术充满热情，性格开朗乐观',
        '小红: 一位经验丰富的AI伦理学家，关注科技发展对社会的影响'
      ],
      admin_analysis: '小明和小红是科技领域的同事，他们正在讨论AI技术的发展方向。小明对新技术充满热情，而小红更关注伦理问题。剧情可以围绕AI技术发展与伦理考量的平衡展开。',
      character_name: '小明'
    };

    addMessage(`发送人物控制器测试数据: ${JSON.stringify(testData)}`);

    try {
      const response = await fetch('http://localhost:5000/api/llm/character_controller', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(testData),
      });

      const data = await response.json();
      addMessage(`人物控制器响应: ${JSON.stringify(data)}`);
      setTestResult('人物控制器测试成功');
    } catch (error) {
      addMessage(`测试失败: ${error instanceof Error ? error.message : String(error)}`);
      setTestResult('人物控制器测试失败');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">LLM API测试页面</h1>
      
      <div className="mb-4">
        <p className="inline-block px-3 py-1 rounded-full bg-blue-100 text-blue-800">
          服务器地址: http://localhost:5000
        </p>
      </div>

      <div className="flex gap-4 mb-4">
        <button 
          onClick={testRoomController}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-blue-300"
          disabled={isLoading}
        >
          {isLoading ? '测试中...' : '测试房间控制器'}
        </button>
        <button 
          onClick={testCharacterController}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:bg-green-300"
          disabled={isLoading}
        >
          {isLoading ? '测试中...' : '测试人物控制器'}
        </button>
      </div>

      {testResult && (
        <div className={`mb-4 p-3 rounded ${testResult.includes('成功') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          {testResult}
        </div>
      )}

      <div className="border border-gray-300 rounded p-4 h-96 overflow-y-auto">
        <h2 className="text-lg font-semibold mb-2">请求/响应记录</h2>
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