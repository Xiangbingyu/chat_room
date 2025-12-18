'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function CreateRoom() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: '',
    worldview: ''
  });
  const [errors, setErrors] = useState<{ name?: string; worldview?: string }>({});
  const [loading, setLoading] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  // 表单输入处理
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // 清除该字段的错误提示
    if (errors[name as keyof typeof errors]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  // 表单验证
  const validateForm = () => {
    const newErrors: { name?: string; worldview?: string } = {};
    
    if (!formData.name.trim()) {
      newErrors.name = '房间名不能为空';
    } else if (formData.name.trim().length < 2) {
      newErrors.name = '房间名至少需要2个字符';
    } else if (formData.name.trim().length > 50) {
      newErrors.name = '房间名不能超过50个字符';
    }
    
    if (!formData.worldview.trim()) {
      newErrors.worldview = '世界观描述不能为空';
    } else if (formData.worldview.trim().length < 10) {
      newErrors.worldview = '世界观描述至少需要10个字符';
    } else if (formData.worldview.trim().length > 1000) {
      newErrors.worldview = '世界观描述不能超过1000个字符';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 表单提交处理
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // 表单验证
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);
    setSubmitError(null);
    
    try {
      // 调用创建房间API
      const response = await fetch('/api/db/rooms', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: formData.name.trim(),
          worldview: formData.worldview.trim()
        })
      });
      
      if (!response.ok) {
        throw new Error('创建房间失败');
      }
      
      const result = await response.json();
      const roomId = result.data.id;
      
      // 创建默认角色：ai管理员
      await fetch('/api/db/characters', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: 'ai管理员',
          description: '负责分析总结人物关系与剧情，引导剧情走向，同时指定下一轮对话的角色，一般在一些事件发生后以及一些人物关系发生变化时出现',
          room_id: roomId
        })
      });
      
      // 创建默认角色：旁白
      await fetch('/api/db/characters', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: '旁白',
          description: '推进剧情，过度，以及环境动作描写等作用',
          room_id: roomId
        })
      });
      
      // 创建成功后跳转到房间页面
      router.push(`/hall/${roomId}`);
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : '创建房间失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background p-4 sm:p-6 lg:p-8">
      <div className="max-w-2xl mx-auto">
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

        {/* 标题 */}
        <h1 className="text-3xl font-bold mb-8 text-foreground">创建新房间</h1>

        {/* 错误提示 */}
        {submitError && (
          <div className="bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 p-4 rounded-lg mb-6">
            {submitError}
          </div>
        )}

        {/* 表单 */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* 房间名 */}
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-foreground mb-1">
              房间名
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="请输入房间名称"
              className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-foreground transition-all ${errors.name ? 'border-red-500 dark:border-red-500' : 'border-zinc-300 dark:border-zinc-600 dark:bg-zinc-700 dark:text-white'}`}
              disabled={loading}
            />
            {errors.name && (
              <p className="text-red-500 text-xs dark:text-red-400 mt-1">{errors.name}</p>
            )}
          </div>

          {/* 世界观 */}
          <div>
            <label htmlFor="worldview" className="block text-sm font-medium text-foreground mb-1">
              世界观描述
            </label>
            <textarea
              id="worldview"
              name="worldview"
              value={formData.worldview}
              onChange={handleInputChange}
              placeholder="请输入房间的世界观描述..."
              rows={6}
              className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-foreground transition-all resize-none ${errors.worldview ? 'border-red-500 dark:border-red-500' : 'border-zinc-300 dark:border-zinc-600 dark:bg-zinc-700 dark:text-white'}`}
              disabled={loading}
            />
            <div className="flex justify-between items-center mt-1">
              {errors.worldview && (
                <p className="text-red-500 text-xs dark:text-red-400">{errors.worldview}</p>
              )}
              <p className="text-zinc-500 text-xs dark:text-zinc-400">
                {formData.worldview.length}/1000
              </p>
            </div>
          </div>

          {/* 操作按钮 */}
          <div className="flex flex-col sm:flex-row gap-4 pt-4">
            <Link
              href="/hall"
              className="inline-flex items-center justify-center h-12 px-6 rounded-lg border border-zinc-300 text-zinc-700 font-medium transition-colors hover:bg-zinc-100 dark:border-zinc-600 dark:text-zinc-300 dark:hover:bg-zinc-700 flex-1"
            >
              取消
            </Link>
            <button
              type="submit"
              className="inline-flex items-center justify-center h-12 px-6 rounded-lg bg-foreground text-background font-medium transition-colors hover:bg-zinc-800 dark:hover:bg-zinc-300 dark:hover:text-zinc-900 flex-1"
              disabled={loading}
            >
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white dark:border-black mx-auto"></div>
              ) : (
                '创建房间'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}