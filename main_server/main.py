import base64
import cv2
import numpy as np
import httpx
from fastapi import FastAPI, WebSocket, Query, Path
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime
from contextlib import asynccontextmanager

# DB 함수 임포트
from db import (
    create_table,
    insert_detection,
    get_detections,
    delete_detection_by_id,
    update_detection_status
)

# 앱 실행 시 호출될 초기화 함수 (테이블 생성 등)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()  # 감지 기록 테이블이 없으면 생성
    yield

# FastAPI 앱 인스턴스 생성
app = FastAPI(lifespan=lifespan)

# WebSocket 엔드포인트: A(client.py)로부터 프레임 수신


@app.websocket("/ws/stream")
async def video_stream(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            # 클라이언트로부터 base64 텍스트 수신
            data = await websocket.receive_text()

            # 디코딩 및 OpenCV 이미지로 변환
            img_data = base64.b64decode(data)
            np_arr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # YOLO 서버에 JPEG 이미지로 전송
            _, img_encoded = cv2.imencode('.jpg', frame)
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://yolo_server:8001/predict",
                    files={
                        "file": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")}
                )
                result = response.json()

            # YOLO 결과를 DB에 저장 (image_path가 있을 경우 포함)
            for detection in result["detections"]:
                label = detection["label"]
                confidence = detection["confidence"]
                bbox = detection["bbox"]
                image_path = detection.get("image_path")  # None or 절대경로
                insert_detection(label, confidence, bbox, image_path)

        except Exception as e:
            print("WebSocket error:", e)
            break

# 감지 결과 조회 API (limit, 라벨, 시간 필터 포함)


@app.get("/get-detections")
def get_detections_api(
    limit: int = Query(10, description="가져올 최대 감지 수"),
    label: Optional[str] = Query(None, description="라벨 필터"),
    start_time: Optional[datetime] = Query(None, description="시작 시간"),
    end_time: Optional[datetime] = Query(None, description="종료 시간")
):
    result = get_detections(limit=limit, label=label,
                            start_time=start_time, end_time=end_time)
    return JSONResponse(content=result)

# 감지 결과 삭제 API


@app.delete("/delete-detection/{detection_id}")
def delete_detection_api(detection_id: int = Path(...)):
    delete_detection_by_id(detection_id)
    return {"message": f"detection {detection_id} deleted"}

# 감지 결과 상태 업데이트 API


@app.put("/update-status/{detection_id}")
def update_status_api(detection_id: int, new_status: str):
    update_detection_status(detection_id, new_status)
    return {"message": f"detection {detection_id} status updated to {new_status}"}
