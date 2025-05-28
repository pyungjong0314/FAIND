import requests
from dotenv import load_dotenv

url = "http://localhost:4000/graphql"  # 여기에 GraphQL 서버 주소를 입력
headers = {"Content-Type": "application/json"}


def post_item_to_main_server(timestamp, location, missing_items ):
    for item in missing_items:
        data = {
            "query": """
                mutation CreateLost($createLostInput: CreateLostInput) {
                    createLost(createLostInput: $createLostInput)
                }
            """,
            "variables": {
                "createLostInput": {
                    "lost_date": timestamp.isoformat(),
                    "lost_location": location,
                    "lost_name": item, 
                    "person_id": 1, # 추후에 광운대 학생/외부인 구분 예정.
                    "status": "found" # found가 분실물인 것.
                }
            }
        }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"[NOTIFIER] Item sent for server → missing: {missing_items}")
        return True
    except requests.RequestException as e:
        print(f"[NOTIFIER] Failed to send alert: {e}")
        return False
