import os

# YOLO 및 DeepSORT 관련 설정
YOLO_MODEL_PATH = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.6

# 저장된 이미지 디렉토리
IMAGE_DIR = "/../images"
os.makedirs(IMAGE_DIR, exist_ok=True)
