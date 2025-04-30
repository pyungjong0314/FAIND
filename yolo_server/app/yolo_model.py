import torch
import cv2
import os
from datetime import datetime

# YOLOv5 모델 로딩
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 저장 디렉토리 설정
SAVE_DIR = "/app/saved_people"
os.makedirs(SAVE_DIR, exist_ok=True)


def run_inference(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = model(rgb_image)

    detections = []

    for *box, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = map(int, box)
        label = model.names[int(cls)]

        # 사람 감지된 경우 이미지 저장
        image_path = None
        if label == "person":
            cropped = image[y1:y2, x1:x2]
            filename = datetime.now().strftime("person_%Y%m%d_%H%M%S.jpg")
            image_path = os.path.abspath(os.path.join(SAVE_DIR, filename))
            cv2.imwrite(image_path, cropped)

        detections.append({
            "label": label,
            "confidence": float(conf),
            "bbox": [x1, y1, x2, y2],
            "image_path": image_path  # 사람이 아닌 경우 None
        })

    return detections
