# Chat Room 后端 API 接口文档

## 1. Java 后端 API

Java 后端负责基础业务逻辑和数据层交互，接口分为 REST 接口（基础）和可改造为 WebSocket 的场景。

### 1.1 Users 接口（用户管理）

#### POST /api/users - 用户创建/注册

**功能**：创建新用户，完成用户初始化。

**请求参数**：
- `username`: string, 必填 - 用户名
- `password`: string, 必填 - 密码

**请求示例**：
```json
{
  "username": "testuser",
  "password": "testpassword123"
}
```

**返回结果**：
```json
{
  "id": "用户ID",
  "username": "用户名",
  "created_at": "创建时间ISO格式"
}
```

### 1.2 Rooms 接口（房间管理）

#### GET /api/rooms - 获取所有房间列表

**功能**：获取所有房间数据，用于构建大厅页面。

**请求参数**：无

**请求示例**：
```bash
curl -X GET http://localhost:8080/api/rooms
```

**返回结果**：
```json
[
  {
    "id": "房间ID",
    "name": "房间名称",
    "worldview": "世界观描述",
    "location": "["地点1","地点2"]",
    "creatorId": "创建者ID",
    "createdAt": "创建时间ISO格式",
    "updatedAt": "更新时间ISO格式"
  }
]
```

#### GET /api/rooms/{roomId} - 获取单个房间详情

**功能**：根据房间 ID 获取单个房间详情（核心是世界观信息），用于进入房间时加载世界观。

**请求参数**：
- `roomId`: string, 必填 - 房间ID（URL路径参数）

**请求示例**：
```bash
curl -X GET http://localhost:8080/api/rooms/123e4567-e89b-12d3-a456-426614174000
```

**返回结果**：
```json
{
  "id": "房间ID",
  "name": "房间名称",
  "worldview": "世界观描述",
  "location": "["地点1","地点2"]",
  "creatorId": "创建者ID",
  "createdAt": "创建时间ISO格式",
  "updatedAt": "更新时间ISO格式"
}
```

#### POST /api/rooms - 创建房间

**功能**：创建新房间。

**请求参数**：
- `name`: string, 必填 - 房间名称
- `worldview`: string, 必填 - 世界观描述
- `location`: array, 可选 - 地点列表

**请求示例**：
```json
{
  "name": "奇幻冒险之旅",
  "worldview": "在一个充满魔法的世界里，勇敢的冒险者们探索未知的领域",
  "location": ["魔法森林", "幽暗洞穴", "神秘城堡"],
  "creator_id": "创建者ID"
}
```

**返回结果**：
```json
{
  "id": "房间ID"
}
```

#### DELETE /api/rooms/{roomId} - 删除房间（可选）

**功能**：删除指定房间，用于清理无效房间。

**请求参数**：
- `roomId`: string, 必填 - 房间ID（URL路径参数）

**请求示例**：
```bash
curl -X DELETE http://localhost:8080/api/rooms/123e4567-e89b-12d3-a456-426614174000
```

**返回结果**：
```json
{
  "status": "success"
}
```

### 1.3 Characters 接口（角色管理）

#### GET /api/characters - 获取房间内所有角色

**功能**：根据请求参数 roomId 查询指定房间内的所有角色，用于进入房间时加载角色列表。

**请求参数**：
- `roomId`: string, 必填 - 房间ID（查询参数）

**请求示例**：
```bash
curl -X GET http://localhost:8080/api/characters?roomId=123e4567-e89b-12d3-a456-426614174000
```

**返回结果**：
```json
[
  {
    "id": "角色ID",
    "name": "角色名称",
    "description": "角色描述",
    "current_location": "当前地点",
    "status": "目前状态",
    "type": "角色类型",
    "room_id": "房间ID",
    "created_at": "创建时间ISO格式"
  }
]
```

#### POST /api/characters - 创建角色

**功能**：创建新角色。

**请求参数**：
- `roomId`: string, 必填 - 房间ID
- `name`: string, 必填 - 角色名称
- `description`: string, 必填 - 角色描述
- `current_location`: string, 可选 - 地点
- `status`: string, 可选 - 目前状态
- `type`: string, 可选 - 角色类型

**请求示例**：
```json
{
  "roomId": "123e4567-e89b-12d3-a456-426614174000",
  "name": "勇者亚瑟",
  "description": "一位勇敢的年轻骑士，发誓要拯救被黑暗笼罩的王国",
  "current_location": "魔法森林入口",
  "status": "开心",
  "type": "角色类型"
}
```

**返回结果**：
```json
{
  "id": "角色ID",
  "name": "角色名称",
  "description": "角色描述",
  "room_id": "房间ID",
  "created_at": "创建时间ISO格式"
}
```

#### DELETE /api/characters/{characterId} - 删除角色（可选）

**功能**：删除指定角色，支持用户修改房间内角色。

**请求参数**：
- `characterId`: string, 必填 - 角色ID（URL路径参数）

**请求示例**：
```bash
curl -X DELETE http://localhost:8080/api/characters/123e4567-e89b-12d3-a456-426614174000
```

**返回结果**：
```json
{
  "status": "success"
}
```

### 1.4 Conversations 接口（对话管理）

#### GET /api/conversations - 获取房间内所有对话

**功能**：根据请求参数 roomId 获取该房间内所有对话记录，用于进入房间时回溯历史对话。

**请求参数**：
- `roomId`: string, 必填 - 房间ID（查询参数）

**请求示例**：
```bash
curl -X GET http://localhost:8080/api/conversations?roomId=123e4567-e89b-12d3-a456-426614174000
```

**返回结果**：
```json
[
  {
    "id": "对话ID",
    "room_id": "房间ID",
    "character_id": "角色ID",
    "character_name": "角色名称",
    "content": "对话内容",
    "current_location": "对话地点",
    "status": "角色状态",
    "next_speaker": "下一个说话角色ID",
    "created_at": "创建时间ISO格式"
  }
]
```

#### POST /api/conversations - 创建/更新对话记录

**功能**：创建或更新对话记录。

**请求参数**：
- `roomId`: string, 必填 - 房间ID
- `characterId`: string, 必填 - 角色ID
- `content`: string, 必填 - 对话内容
- `current_location`: string, 可选 - 对话发生地点
- `status`: string, 可选 - 对话状态
- `next_speaker`: string, 可选 - 下一个说话的角色ID

**请求示例**：
```json
{
  "roomId": "123e4567-e89b-12d3-a456-426614174000",
  "characterId": "123e4567-e89b-12d3-a456-426614174001",
  "content": "我已经准备好开始冒险了！",
  "current_location": "魔法森林入口",
  "status": "开心",
  "next_speaker": "123e4567-e89b-12d3-a456-426614174002"
}
```

**返回结果**：
```json
{
  "id": "对话ID",
  "room_id": "房间ID",
  "character_id": "角色ID",
  "character_name": "角色名称",
  "content": "对话内容",
  "current_location": "对话地点",
  "status": "角色状态",
  "next_speaker": "下一个说话角色ID",
  "created_at": "创建时间ISO格式"
}
```

## 2. Python 后端 API

Python 后端负责大模型业务逻辑，核心是对接大模型的两个能力接口。

### 2.1 AI 管理员接口

#### POST /api/ai/admin - AI 管理员分析与引导

**功能**：分析总结人物关系与剧情，引导剧情走向，同时指定下一轮对话的角色。

**请求参数**：
- `roomId`: string, 必填 - 房间ID
- `characterId`: string, 必填 - 角色ID
- `history_dialogues`: string, 必填 - 上一句的回复内容
- `character_settings`: array[string], 必填 - 所有人物设定列表
- `worldview`: string, 必填 - 世界观描述
- `previous_speaker_id`: string, 必填 - 上一轮说话角色的ID
- `previous_speaker_name`: string, 必填 - 上一轮说话角色的姓名
- `previous_speaker_location`: string, 必填 - 上一轮对话的发生地点
- `previous_speaker_status`: string, 必填 - 上一轮对话时的角色状态

**请求示例**：
```json
{
  "roomId": "123e4567-e89b-12d3-a456-426614174000",
  "characterId": "123e4567-e89b-12d3-a456-426614174001",
  "history_dialogues": "法师梅林：祝你好运，勇者。",
  "character_settings": [
    "勇者亚瑟：一位年轻勇敢的骑士，发誓要拯救被黑暗笼罩的王国",
    "法师梅林：一位古老的法师，拥有强大的魔法力量，是亚瑟的导师",
    "黑暗领主：试图统治整个王国的邪恶存在，拥有黑暗之剑"
  ],
  "worldview": "在一个充满魔法的中世纪王国里，黑暗领主正在威胁整个世界。只有找到传说中的黑暗之剑，才能击败黑暗领主，拯救王国。",
  "previous_speaker_id": "123e4567-e89b-12d3-a456-426614174002",
  "previous_speaker_name": "法师梅林",
  "previous_speaker_location": "法师塔",
  "previous_speaker_status": "神秘"
}
```

**返回结果**：
```json
{
  "message": "AI管理员接口已处理请求",
  "roomId": admin_request.roomId,
  "characterId": admin_request.characterId,
  "core_memory": core_memory,
  "prompt": prompt,
  "ai_response": ai_response,
  "total_dialogues": total_dialogues
}
```

### 2.2 AI 扮演者接口

#### POST /api/ai/actor - AI 角色扮演

**功能**：扮演指定的角色做出回复，同时指定下一轮对话的角色。

**请求参数**：
- `roomId`: string, 必填 - 房间ID
- `characterId`: string, 必填 - 角色ID
- `history_dialogues`: string, 必填 - 上一句的回复内容
- `character_settings`: array[string], 必填 - 所有人物设定列表
- `worldview`: string, 必填 - 世界观描述
- `character_name`: string, 必填 - 扮演的角色名称
- `current_location`: string, 必填 - 对话发生地点
- `status`: string, 必填 - 对话状态
- `previous_speaker_id`: string, 必填 - 上一轮说话角色的ID
- `previous_speaker_name`: string, 必填 - 上一轮说话角色的姓名
- `previous_speaker_location`: string, 必填 - 上一轮对话的发生地点
- `previous_speaker_status`: string, 必填 - 上一轮对话时的角色状态

**请求示例**：
```json
{
  "roomId": "123e4567-e89b-12d3-a456-426614174000",
  "characterId": "123e4567-e89b-12d3-a456-426614174002",
  "history_dialogues": "角色A：那我们出发吧！",
  "character_settings": [
    "角色A：一个活泼开朗的年轻人，喜欢户外活动。",
    "角色B：一个细心周到的朋友，对周围环境很熟悉。"
  ],
  "worldview": "这是一个现代都市的世界观，人们过着普通的生活，有公园、街道、商店等常见的城市设施。",
  "character_name": "角色B",
  "current_location": "公园",
  "status": "正在前往公园",
  "previous_speaker_id": "123e4567-e89b-12d3-a456-426614174003",
  "previous_speaker_name": "角色A",
  "previous_speaker_location": "公交车站",
  "previous_speaker_status": "兴奋"
}
```

**返回结果**：
```json
{
  "message": "AI管理员接口已处理请求",
  "roomId": admin_request.roomId,
  "characterId": admin_request.characterId,
  "core_memory": core_memory,
  "prompt": prompt,
  "ai_response": ai_response,
  "total_dialogues": total_dialogues
}
```

## 3. WebSocket 改造场景

### 3.1 Java 后端 WebSocket 改造点

#### 房间内对话的实时推送

- 将 `POST /api/conversations` 和 `GET /api/conversations` 改造为 WebSocket 连接
- 当用户或 AI 发送新对话时，服务端主动将对话内容推送给当前房间的所有连接客户端
- 无需客户端轮询获取最新对话，提升房间内的交互实时性

#### 房间状态同步（可选）

- 若扩展为多用户同房间协作创作，可通过 WebSocket 同步房间的角色状态、剧情进度等
- 确保多用户视角一致

### 3.2 Python 后端 WebSocket 改造点

#### AI 回复的实时流式返回

- 将 `POST /api/ai/admin` 和 `POST /api/ai/actor` 改造为 WebSocket 接口
- 大模型生成回复（尤其是长剧情、多角色台词）时，通过 WebSocket 分段推送生成的内容
- 避免客户端等待完整结果的卡顿，提升用户体验

#### 剧情推进指令的实时触发

- AI 管理员生成 "下一轮对话角色" 指令后，通过 WebSocket 直接触发 AI 扮演者的回复逻辑
- 减少 HTTP 接口的调用链路，提升剧情流转的流畅度

### 3.3 跨端联动的 WebSocket 场景

- 搭建 Java 和 Python 后端的 WebSocket 联动通道
- Java 端监听房间对话的 WebSocket 事件，当触发 AI 调用逻辑时，直接通过内部 WebSocket 通知 Python 端发起大模型请求
- Python 端将 AI 回复通过 WebSocket 推送给 Java 端，再由 Java 端推送给前端，形成完整的实时交互闭环

## 4. 特殊角色说明

每个房间除了玩家设定的角色以外，还有两个默认特殊角色：

1. **AI 管理员**：用于分析剧情，推进剧情发展
2. **旁白**：用于辅助推进剧情或者进行一些环境描写