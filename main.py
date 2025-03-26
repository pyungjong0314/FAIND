from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np
import base64
from yolo import run_yolo_on_frame, IMAGE_DIR, entry_persons, exit_persons

app = FastAPI()
app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")


@app.websocket("/ws/stream")
async def video_stream(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            img_data = base64.b64decode(data)
            np_arr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            run_yolo_on_frame(frame)
        except Exception as e:
            print("WebSocket error:", e)
            break


@app.get("/get-images")
def get_images():
    return {
        "entry_persons": [
            {"image": f"http://127.0.0.1:8000/images/{p['image']}", "items": p["items"]}
            for p in entry_persons
        ],
        "exit_persons": [
            {"image": f"http://127.0.0.1:8000/images/{p['image']}", "items": p["items"]}
            for p in exit_persons
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
