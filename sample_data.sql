-- 添加示例数据到short_term_memories表
INSERT INTO short_term_memories (id, room_id, content, created_at, updated_at)
VALUES 
('1', 'room_001', '用户询问了关于AI角色设定的问题', datetime('now'), datetime('now')),
('2', 'room_002', '角色A和角色B讨论了世界观设定', datetime('now'), datetime('now'));

-- 添加示例数据到long_term_memories表
INSERT INTO long_term_memories (id, room_id, content, embedding, created_at, updated_at)
VALUES 
('3', 'room_001', '用户喜欢科幻题材，偏好详细的角色背景', X'00000000', datetime('now'), datetime('now')),
('4', 'room_002', '角色A对魔法系统有深入了解', X'11111111', datetime('now'), datetime('now'));

-- 添加示例数据到conversation_histories表
INSERT INTO conversation_histories (id, room_id, character_id, character_name, content, current_location, status, created_at, updated_at)
VALUES 
('5', 'room_001', 'char_001', 'AI管理员', '欢迎来到聊天房间！', '大厅', 'active', datetime('now'), datetime('now')),
('6', 'room_001', 'user_001', '用户', '你好，我想创建一个科幻角色', '大厅', 'active', datetime('now'), datetime('now')),
('7', 'room_002', 'char_002', '魔法师', '这里是魔法学院的图书馆', '图书馆', 'active', datetime('now'), datetime('now'));

-- 添加示例数据到admin_analysis_records表
INSERT INTO admin_analysis_records (id, room_id, character_id, analysis_content, created_at, updated_at)
VALUES 
('8', 'room_001', 'char_001', '用户需要帮助创建科幻角色，应提供详细的角色模板', datetime('now'), datetime('now')),
('9', 'room_002', 'char_002', '魔法师角色适合深入探讨魔法系统设定', datetime('now'), datetime('now'));