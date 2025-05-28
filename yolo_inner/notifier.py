import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEB_SERVER_URL = os.getenv(
    "WEB_SERVER_URL", "http://localhost:9000/report-lost")


def send_lost_to_web_server(lost_json: str):
    try:
        response = requests.post(
            WEB_SERVER_URL,
            data=lost_json,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        print("[NOTIFIER] Lost objects sent successfully.")
    except requests.RequestException as e:
        print(f"[NOTIFIER] Failed to send lost objects: {e}")
