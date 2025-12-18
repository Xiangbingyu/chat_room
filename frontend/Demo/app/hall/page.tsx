'use client';

import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';

interface Room {
  id: string;
  name: string;
  worldview: string;
  created_at: string;
}

export default function Hall() {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // 获取所有房间信息
    const fetchRooms = async () => {
      try {
        const response = await fetch('/api/db/rooms');
        if (!response.ok) {
          throw new Error('Failed to fetch rooms');
        }
        const data = await response.json();
        setRooms(data.data || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch rooms');
      } finally {
        setLoading(false);
      }
    };

    fetchRooms();
  }, []);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-black font-sans">
      <main className="max-w-6xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        {/* 页面标题和创建按钮 */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
          <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
            房间大厅
          </h1>
          <Link
            href="/hall/create_room"
            className="inline-flex items-center justify-center h-12 px-6 rounded-full bg-foreground text-background font-medium transition-colors hover:bg-zinc-800 dark:hover:bg-zinc-300"
          >
            创建房间
          </Link>
        </div>

        {/* 错误提示 */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-8 dark:bg-red-900/30 dark:border-red-800 dark:text-red-300">
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        {/* 加载状态 */}
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-zinc-900 dark:border-white"></div>
          </div>
        ) : (
          /* 房间列表 */
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {rooms.length > 0 ? (
              rooms.map((room) => (
                <Link
                  key={room.id}
                  href={`/hall/${room.id}`}
                  className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden dark:bg-zinc-800 dark:border border-zinc-700"
                >
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-3">
                      <h2 className="text-xl font-semibold text-zinc-900 dark:text-white">
                        {room.name}
                      </h2>
                      <span className="text-sm text-zinc-500 dark:text-zinc-400">
                        {formatDate(room.created_at)}
                      </span>
                    </div>
                    <p className="text-zinc-600 dark:text-zinc-300 line-clamp-3 mb-4">
                      {room.worldview}
                    </p>
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium text-zinc-500 dark:text-zinc-400">
                        进入房间
                      </span>
                      <svg
                        className="w-5 h-5 text-zinc-400 group-hover:text-zinc-600 dark:text-zinc-500 dark:group-hover:text-zinc-300"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M17 8l4 4m0 0l-4 4m4-4H3"
                        />
                      </svg>
                    </div>
                  </div>
                </Link>
              ))
            ) : (
              /* 无房间提示 */
              <div className="col-span-full bg-white rounded-lg shadow-md p-12 text-center dark:bg-zinc-800 dark:border border-zinc-700">
                <svg
                  className="w-16 h-16 mx-auto text-zinc-400 mb-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01"
                  />
                </svg>
                <h3 className="text-xl font-medium text-zinc-900 dark:text-white mb-2">
                  暂无房间
                </h3>
                <p className="text-zinc-600 dark:text-zinc-400 mb-6">
                  还没有创建任何房间，快来创建第一个房间吧！
                </p>
                <Link
                  href="/hall/create_room"
                  className="inline-flex items-center justify-center h-10 px-4 rounded-md bg-foreground text-background font-medium transition-colors hover:bg-zinc-800 dark:hover:bg-zinc-300"
                >
                  创建房间
                </Link>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
