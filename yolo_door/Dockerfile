FROM python:3.10-slim

# 필수 시스템 패키지 설치
RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    git \
    build-essential \
    libgl1 \
    python3-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    && apt-get clean

RUN pip install --upgrade pip

# 미리 필요한 패키지 설치 (deep-person-reid)
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    Cython \
    h5py \
    Pillow \
    six \
    scipy \
    opencv-python \
    matplotlib \
    tb-nightly \
    future \
    yacs \
    gdown \
    flake8 \
    yapf \
    isort==4.3.21 \
    imageio \
    chardet

# torch 등 미리 설치
RUN pip install --no-cache-dir \
    torch==2.0.1 \
    torchvision==0.15.2 \
    torchaudio

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
