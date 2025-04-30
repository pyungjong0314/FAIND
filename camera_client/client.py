import cv2
import asyncio
import websockets
import base64

# main_server가 Docker에서 포트 8000으로 열려 있다면
# 로컬에서 실행 시 http://localhost 또는 실제 IP로 접근
# 서버가 같은 컴퓨터 내 Docker라면 localhost 가능
# 다른 컴퓨터에 서버가 있을 경우 해당 컴퓨터의 IP 주소로 수정
uri = "ws://main_server:8000/ws/stream"


async def send_video():
    # 카메라 연결 (Windows에서도 기본 카메라 0번)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ 카메라를 열 수 없습니다.")
        return

    async with websockets.connect(uri, max_size=None) as websocket:
        print("✅ WebSocket 연결 완료. 영상 전송 시작.")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ 프레임 읽기 실패.")
                break

            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            await websocket.send(jpg_as_text)

# Windows에서 실행
if __name__ == "__main__":
    asyncio.run(send_video())
