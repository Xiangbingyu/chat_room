from typing import List
from pydantic import BaseModel


class AdminRequest(BaseModel):
    roomId: str
    characterId: str
    history_dialogues: str
    character_settings: List[str]
    worldview: str
    previous_speaker_id: str
    previous_speaker_name: str
    previous_speaker_location: str
    previous_speaker_status: str


class AdminResponse(BaseModel):
    roomId: str
    characterId: str
    response_content: str
    next_speaker: str


class ActorRequest(BaseModel):
    roomId: str
    characterId: str
    history_dialogues: str
    character_settings: List[str]
    worldview: str
    character_name: str
    current_location: str
    status: str
    previous_speaker_id: str
    previous_speaker_name: str
    previous_speaker_location: str
    previous_speaker_status: str


class ActorResponse(BaseModel):
    roomId: str
    characterId: str
    response_content: str
    next_speaker: str
    current_location: str
    status: str
