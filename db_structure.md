# AI Chat Room 数据库表结构设计

## 1. Users 表（用户表）

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|-----|------|
| id | VARCHAR(36) | PRIMARY KEY | 用户唯一标识（UUID） |
| username | VARCHAR(50) | NOT NULL, UNIQUE | 用户名 |
| password | VARCHAR(255) | NOT NULL | 密码（加密存储） |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 2. Rooms 表（房间表）

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|-----|------|
| id | VARCHAR(36) | PRIMARY KEY | 房间唯一标识（UUID） |
| name | VARCHAR(100) | NOT NULL | 房间名称 |
| worldview | TEXT | NOT NULL | 世界观描述 |
| location | JSON | NULL | 地点列表 |
| creator_id | VARCHAR(36) | NOT NULL, FOREIGN KEY REFERENCES Users(id) | 创建者ID |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 3. Characters 表（角色表）

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|-----|------|
| id | VARCHAR(36) | PRIMARY KEY | 角色唯一标识（UUID） |
| name | VARCHAR(50) | NOT NULL | 角色名称 |
| description | TEXT | NOT NULL | 角色描述/设定 |
| room_id | VARCHAR(36) | NOT NULL, FOREIGN KEY REFERENCES Rooms(id) | 所属房间ID |
| current_location | VARCHAR(100) | NULL | 当前地点 |
| status | VARCHAR(50) | NULL | 角色状态 |
| type | VARCHAR(20) | NOT NULL, DEFAULT 'user' | 角色类型（user/ai_admin/narrator） |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 4. Conversations 表（对话表）

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|-----|------|
| id | VARCHAR(36) | PRIMARY KEY | 对话唯一标识（UUID） |
| room_id | VARCHAR(36) | NOT NULL, FOREIGN KEY REFERENCES Rooms(id) | 所属房间ID |
| character_id | VARCHAR(36) | NOT NULL, FOREIGN KEY REFERENCES Characters(id) | 发言角色ID |
| content | TEXT | NOT NULL | 对话内容 |
| current_location | VARCHAR(100) | NULL | 当前地点 |
| status | VARCHAR(50) | NULL | 状态 |
| next_speaker | VARCHAR(36) | NULL | 下个说话的人角色ID |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 表关系说明

1. Users 和 Rooms：
   - 用户可以创建多个房间（一对多关系）
   - 可以在Rooms表中添加创建者字段：creator_id VARCHAR(36) FOREIGN KEY REFERENCES Users(id)

2. Rooms 和 Characters：
   - 一个房间包含多个角色（一对多关系）
   - 每个角色必须属于一个房间

3. Rooms 和 Conversations：
   - 一个房间包含多个对话（一对多关系）
   - 每个对话必须属于一个房间

4. Characters 和 Conversations：
   - 一个角色可以参与多个对话（一对多关系）
   - 每个对话必须由一个角色发起

## 特殊角色说明

每个房间会默认创建两个特殊角色：
1. AI管理员（type='ai_admin'）：用于分析剧情，推进剧情发展
2. 旁白（type='narrator'）：用于辅助推进剧情或进行环境描写

## 索引建议

1. Users表：username字段添加唯一索引
2. Rooms表：created_at字段添加索引，用于按时间排序房间列表
3. Characters表：room_id字段添加索引，用于快速查询房间内角色
4. Conversations表：room_id和created_at字段添加联合索引，用于按时间排序房间内对话

---

# Python端数据库结构（SQLite + sqlite-vec）

## 1. ShortTermMemories 表（短期记忆表）

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|-----|------|
| id | VARCHAR(36) | PRIMARY KEY | 短期记忆唯一标识（UUID） |
| room_id | VARCHAR(36) | NOT NULL | 所属房间ID |
| content | TEXT | NOT NULL | 经过大模型压缩的邻近对话信息 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 2. LongTermMemories 表（长期记忆表）

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|-----|------|
| id | VARCHAR(36) | PRIMARY KEY | 长期记忆唯一标识（UUID） |
| room_id | VARCHAR(36) | NOT NULL | 所属房间ID |
| content | TEXT | NOT NULL | 原始记忆内容 |
| embedding | VEC(1536) | NOT NULL | 内容的向量表示（使用sqlite-vec） |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 3. ConversationHistories 表（历史对话表）

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|-----|------|
| id | VARCHAR(36) | PRIMARY KEY | 对话历史唯一标识（UUID） |
| room_id | VARCHAR(36) | NOT NULL | 所属房间ID |
| character_id | VARCHAR(36) | NOT NULL | 发言角色ID |
| character_name | VARCHAR(50) | NOT NULL | 发言角色名称 |
| content | TEXT | NOT NULL | 对话内容 |
| current_location | VARCHAR(100) | NULL | 当前地点 |
| status | VARCHAR(50) | NULL | 角色状态 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 4. AdminAnalysisRecords 表（AI管理员分析记录表）

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|-----|------|
| id | VARCHAR(36) | PRIMARY KEY | 分析记录唯一标识（UUID） |
| room_id | VARCHAR(36) | NOT NULL | 所属房间ID |
| character_id | VARCHAR(36) | NOT NULL | 相关角色ID |
| analysis_content | TEXT | NOT NULL | 管理员分析内容 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 5. 核心记忆（内存块存储）

核心记忆通过内存块实时存储，不持久化到数据库，包含以下内容：

| 字段名 | 数据类型 | 描述 |
|-------|---------|------|
| room_id | str | 所属房间ID |
| recent_conversations | List[Dict] | 近10轮详细对话记录 |
| character_settings | Dict | 人物设定 |
| worldview | Text | 世界观描述 |
| locations | List[str] | 世界的可选地点 |
| admin_analysis | Text | 当前管理员分析结果 |
| character_name | str | 扮演角色姓名 |
| current_location | str | 当前地点 |
| character_status | str | 角色状态 |
| next_speaker | str | 下一个发言角色ID |

## Python端数据库索引建议

1. ShortTermMemories表：room_id和created_at字段添加联合索引，用于快速查询特定房间的最新短期记忆
2. LongTermMemories表：room_id字段添加索引，用于区分不同房间的记忆
3. LongTermMemories表：创建基于embedding字段的向量索引，用于RAG查询和相似度匹配
4. ConversationHistories表：room_id和created_at字段添加联合索引，用于按时间查询房间对话历史
5. ConversationHistories表：room_id和character_id字段添加联合索引，用于查询特定房间内特定角色的所有对话
6. AdminAnalysisRecords表：room_id和created_at字段添加联合索引，用于快速查询特定房间的最新管理员分析结果
7. AdminAnalysisRecords表：room_id和character_id字段添加联合索引，用于查询特定房间内特定角色的所有分析记录

## 表关系说明

1. 短期记忆、长期记忆和对话历史都与Rooms表关联，通过room_id字段区分不同房间
2. 短期记忆用于存储压缩后的近期对话，支持快速查询
3. 长期记忆使用向量数据库存储，支持相似度查询和RAG应用
4. 对话历史存储完整的原始对话记录，用于回溯和分析
5. 核心记忆在内存中实时维护，包含最新的会话状态和关键信息