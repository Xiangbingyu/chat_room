from typing import List, Dict, Optional
from pydantic import BaseModel


# AI管理员接口 - 请求数据格式
class AdminRequest(BaseModel):
    roomId: str  # 房间ID
    characterId: str  # 角色ID
    history_dialogues: str  # 上一句的回复内容
    character_settings: List[str]  # 人物设定列表
    worldview: str  # 世界观描述


# AI管理员接口 - 响应数据格式
class AdminResponse(BaseModel):
    roomId: str  # 房间ID
    characterId: str  # 角色ID
    response_content: str  # 管理员回复内容
    next_speaker: str  # 下一轮对话角色


# AI扮演者接口 - 请求数据格式
class ActorRequest(BaseModel):
    roomId: str  # 房间ID
    characterId: str  # 角色ID
    history_dialogues: str  # 上一句的回复内容
    character_settings: List[str]  # 人物设定列表
    worldview: str  # 世界观描述
    character_name: str  # 扮演的角色名称
    current_location: str  # 对话发生地点
    status: str  # 对话状态

# AI扮演者接口 - 响应数据格式
class ActorResponse(BaseModel):
    roomId: str  # 房间ID
    characterId: str  # 角色ID
    response_content: str  # 角色回复内容
    next_speaker: str  # 下一轮对话角色
    current_location: str  # 对话发生地点
    status: str  # 对话状态
