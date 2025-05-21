import requests
import os
from dotenv import load_dotenv

# .env에서 MAIN_SERVER_URL 로드
load_dotenv()
MAIN_SERVER_URL = os.getenv(
    "MAIN_SERVER_URL", "http://localhost:9000/post-alert")


def send_alert_to_main_server(person_id, missing_items):
    data = {
        "person_id": person_id,
        "missing_items": missing_items
    }
    try:
        response = requests.post(MAIN_SERVER_URL, json=data)
        response.raise_for_status()
        print(
            f"[NOTIFIER] Alert sent for person {person_id} → missing: {missing_items}")
        return True
    except requests.RequestException as e:
        print(f"[NOTIFIER] Failed to send alert: {e}")
        return False
