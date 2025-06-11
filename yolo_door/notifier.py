import requests
from dotenv import load_dotenv
from dictionary import CLASS_NAME_KOR
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

url = "http://host.docker.internal:4000/graphql"  # 여기에 GraphQL 서버 주소를 입력 docker 내부에서는 localhost가 host.docker.internal로 바뀜.
headers = {"Content-Type": "application/json"}


def post_item_to_main_server(timestamp, location, missing_items, items_detail):
    for item in missing_items:
        data = {
            "query": """
                mutation CreateLost($createLostInput: CreateLostInput) {
                    createLost(createLostInput: $createLostInput)
                }
            """,
            "variables": {
                "createLostInput": {
                    "lost_name": CLASS_NAME_KOR.get(item, item), # 영어에서 한국어로 바꿔줌
                    "lost_location": location,
                    "lost_date": timestamp.isoformat(),
                    "status": "found", # found가 분실물인 것.
                    "lost_image": f"images/items/{items_detail[item]}_{item}.jpg",
                    "person_id": 1, # 추후에 광운대 학생/외부인 구분 예정.
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

def send_faind_email(subject, item_name, location, timestamp, to_email, from_email, from_password, smtp_server='smtp.gmail.com', smtp_port=587):
    try:
        # HTML 본문 생성
        html = f"""
        <html>
        <head>
            <style>
                .container {{
                    font-family: Arial, sans-serif;
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 10px;
                    border: 1px solid #dee2e6;
                    max-width: 600px;
                    margin: auto;
                }}
                .header {{
                    font-size: 22px;
                    font-weight: bold;
                    color: #343a40;
                    margin-bottom: 10px;
                }}
                .body {{
                    font-size: 16px;
                    color: #495057;
                    margin-bottom: 20px;
                }}
                .footer {{
                    font-size: 13px;
                    color: #868e96;
                    border-top: 1px solid #ced4da;
                    padding-top: 10px;
                }}
                .highlight {{
                    color: #0d6efd;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">FAIND 분실물 알림</div>
                <div class="body">
                    <p><span class="highlight">{location}</span>에서 <span class="highlight">{item_name}</span>이(가) 분실된 것으로 감지되었습니다.</p>
                    <p>감지 시각: <span class="highlight">{timestamp}</span></p>
                    <p>https://faind-ten.vercel.app/ 에서 확인하실 수 있습니다.</p>
                </div>
                <div class="footer">
                    이 메일은 FAIND 분실물 탐지 시스템에 의해 자동으로 발송되었습니다.
                </div>
            </div>
        </body>
        </html>
        """

        # MIME 구성
        message = MIMEMultipart("alternative")
        message["From"] = from_email
        message["To"] = to_email
        message["Subject"] = subject

        # HTML 형식 추가
        message.attach(MIMEText(html, "html"))

        # SMTP 전송
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(message)
        server.quit()

        print("FAIND 메일이 전송되었습니다.")

    except Exception as e:
        print(f"메일 전송 실패: {e}")

# send_faind_email(
#     subject="FAIND - 분실물 감지 알림",
#     item_name="검정색 우산",
#     location="도서관 3층 12번 책상",
#     timestamp="2025-05-30 14:37:22",
#     to_email = "sonopj@kw.ac.kr",
#     from_email = "2025kwchambit@gmail.com",
#     from_password = "nnjnboypqhiakroo"
# )
