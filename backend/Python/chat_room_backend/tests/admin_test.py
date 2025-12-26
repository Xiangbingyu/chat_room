import requests
import json

url = 'http://localhost:8000/api/ai/admin'

test_data = {
    "roomId": "test-room-001",
    "characterId": "admin-001",
    "history_dialogues": "你好，我想了解一下这个聊天室的功能",
    "character_settings": [
        "AI管理员，负责回答用户问题",
        "友好、专业、耐心",
        "熟悉聊天室的所有功能"
    ],
    "worldview": "这是一个虚拟的聊天室世界，用户可以在这里交流、互动",
    "previous_speaker_id": "user-001",
    "previous_speaker_name": "用户张三",
    "previous_speaker_location": "聊天室大厅",
    "previous_speaker_status": "在线"
}

def test_ai_admin_api():
    try:
        response = requests.post(url, json=test_data)
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    test_ai_admin_api()