# YOLO Inner Dockerfile
FROM python:3.9-slim

# 필수 패키지 설치
RUN apt-get update && \
    apt-get install -y git ffmpeg libsm6 libxext6 libgl1-mesa-glx && \
    apt-get clean

# 작업 디렉토리 생성
WORKDIR /app

# requirements 설치
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# 코드 복사
COPY app/ ./app/
WORKDIR /app/app

# 실행 명령
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
