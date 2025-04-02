# client.py
import cv2
import asyncio
import websockets
import base64


async def send_video():
    uri = "ws://B_IP:8000/ws/stream"
    async with websockets.connect(uri, max_size=None) as websocket:
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            await websocket.send(jpg_as_text)

asyncio.run(send_video())
