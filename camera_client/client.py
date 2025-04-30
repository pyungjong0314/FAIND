import cv2
import asyncio
import websockets
import base64

# 비동기 함수: 카메라 프레임을 WebSocket으로 전송


async def send_video():
    # WebSocket 서버 주소 (main_server의 /ws/stream 엔드포인트)
    uri = "ws://main_server:8000/ws/stream"

    # WebSocket 연결 (max_size=None은 메시지 크기 제한 없음)
    async with websockets.connect(uri, max_size=None) as websocket:
        # 기본 웹캠(장치 번호 0)으로부터 비디오 캡처 시작
        cap = cv2.VideoCapture(0)

        while True:
            # 프레임을 하나 읽어옴
            ret, frame = cap.read()

            # 프레임을 못 읽으면 루프 종료 (카메라 연결 끊긴 경우 등)
            if not ret:
                break

            # 프레임을 JPEG 형식으로 인코딩
            _, buffer = cv2.imencode('.jpg', frame)

            # 인코딩된 이미지(바이트)를 Base64 문자열로 변환
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')

            # WebSocket을 통해 서버로 전송
            await websocket.send(jpg_as_text)

if __name__ == "__main__":
    asyncio.run(send_video())
