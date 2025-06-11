from fastapi import APIRouter, WebSocket
import base64
import cv2
import numpy as np


ws_router = APIRouter()


@ws_router.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            from video_processor import frame_queue
            data = await websocket.receive_text()
            img_data = base64.b64decode(data)
            np_arr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is not None and not frame_queue.full():
                from video_processor import process_frame
                process_frame(frame)
    except Exception as e:
        print(f"[WebSocket] Connection closed or error occurred: {e}")
        await websocket.close()
