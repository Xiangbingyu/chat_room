import requests
import json

url = 'http://localhost:8000/api/ai/actor'

test_data = {
    "roomId": "test-room-001",
    "characterId": "actor-001",
    "history_dialogues": "你好，请问你是谁？",
    "character_settings": [
        "张三，一个热情开朗的年轻人",
        "喜欢帮助别人，乐于助人",
        "说话幽默风趣，喜欢开玩笑",
        "对生活充满热情，积极乐观"
    ],
    "worldview": "这是一个现代都市背景的聊天室，人们在这里交流生活、工作和兴趣爱好",
    "character_name": "张三",
    "current_location": "聊天室大厅",
    "status": "在线",
    "previous_speaker_id": "user-001",
    "previous_speaker_name": "用户李四",
    "previous_speaker_location": "聊天室大厅",
    "previous_speaker_status": "在线"
}

def test_ai_actor_api():
    try:
        response = requests.post(url, json=test_data)
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    test_ai_actor_api()