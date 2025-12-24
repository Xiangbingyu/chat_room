import requests
import json

url = 'http://localhost:8000/api/memory/cleanup'

test_data = {
    "room_id": "test-room-001"
}

def test_memory_cleanup_api():
    try:
        response = requests.post(url, json=test_data)
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    test_memory_cleanup_api()