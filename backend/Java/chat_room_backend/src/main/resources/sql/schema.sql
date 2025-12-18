-- 创建Users表
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建Rooms表
CREATE TABLE IF NOT EXISTS rooms (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    worldview TEXT NOT NULL,
    location JSON,
    creator_id VARCHAR(36) NOT NULL REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建Characters表
CREATE TABLE IF NOT EXISTS characters (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    room_id VARCHAR(36) NOT NULL REFERENCES rooms(id),
    current_location VARCHAR(100),
    status VARCHAR(50),
    type VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建Conversations表
CREATE TABLE IF NOT EXISTS conversations (
    id VARCHAR(36) PRIMARY KEY,
    room_id VARCHAR(36) NOT NULL REFERENCES rooms(id),
    character_id VARCHAR(36) NOT NULL REFERENCES characters(id),
    content TEXT NOT NULL,
    current_location VARCHAR(100),
    status VARCHAR(50),
    next_speaker VARCHAR(36) REFERENCES characters(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_rooms_created_at ON rooms(created_at);
CREATE INDEX IF NOT EXISTS idx_characters_room_id ON characters(room_id);
CREATE INDEX IF NOT EXISTS idx_conversations_room_id_created_at ON conversations(room_id, created_at);