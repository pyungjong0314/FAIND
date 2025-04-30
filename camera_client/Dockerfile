FROM python:3.10

WORKDIR /app

COPY client.py .

RUN pip install opencv-python websockets

CMD ["python", "client.py"]
