from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2
from app.yolo_model import run_inference  # YOLO 추론 함수

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

# POST /predict: 이미지 업로드를 받아 객체 감지를 수행하는 엔드포인트


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 업로드된 이미지 파일을 비동기적으로 읽음
    contents = await file.read()

    # 바이트 데이터를 numpy 배열로 변환
    np_arr = np.frombuffer(contents, np.uint8)

    # numpy 배열을 OpenCV 이미지(BGR)로 디코딩
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # YOLO 모델로 감지 수행
    detections = run_inference(image)

    # 감지 결과를 JSON 형태로 반환
    return {"detections": detections}
