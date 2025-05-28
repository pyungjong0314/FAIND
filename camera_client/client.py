import cv2
import asyncio
import websockets
import base64

# WebSocket 서버 주소 (실제 서버 주소 사용하기. 추후 env로 분리)
uri = "ws://main_server:8000/ws/stream" 

async def send_video():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    async with websockets.connect(uri, max_size=None) as websocket:
        print("WebSocket 연결 완료. 영상 전송 시작.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("프레임 읽기 실패.")
                break

            # 인코딩 후 Base64로 전송
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            await websocket.send(jpg_as_text)

            # 지연 시간: 100ms (초당 5~10장)
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(send_video())
