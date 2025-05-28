from fastapi import APIRouter, WebSocket
import base64
import numpy as np
import cv2
from processor_adapter import process_frame

ws_router = APIRouter()


@ws_router.websocket("/ws/stream2")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            img_data = base64.b64decode(data)
            np_arr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is not None:
                process_frame(frame)
    except Exception as e:
        print(f"[WebSocket] Error: {e}")
        await websocket.close()
