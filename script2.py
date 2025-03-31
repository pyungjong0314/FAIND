from fastapi import FastAPI
from fastapi.responses import FileResponse
import cv2
import datetime
import numpy as np
import os
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# YOLOv8 모델 및 DeepSORT 초기화
model = YOLO("yolov8n.pt")
tracker = DeepSort(max_age=50)

CONFIDENCE_THRESHOLD = 0.6
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (0, 0, 255)

# 얼굴 검출 모델 로드 (OpenCV Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# 저장된 이미지 폴더
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# 입출입 선 위치
OUTSIDE_LINE = None  # 왼쪽 1/3 위치
INSIDE_LINE = None      # 오른쪽 2/3 위치

# 이동 방향 판별을 위한 클래스
class Person:
    def __init__(self, track_id, first_location):
        self.track_id = track_id
        self.passed_lines = []  # "entrance" 또는 "exit" 기록
        self.direction = None   # "entry" 또는 "exit"
        self.first_location = first_location # 처음 감지된 위치
        self.items = set()

    def update_position(self, center_x):
        """현재 사람 객체가 어떤 선을 통과했는지 기록"""
        
        if self.first_location < OUTSIDE_LINE: # 왼쪽에서 처음 감지되었을 때
            if center_x > OUTSIDE_LINE and "outside" not in self.passed_lines:
                self.passed_lines.append("outside")
            elif center_x > INSIDE_LINE and "inside" not in self.passed_lines:
                self.passed_lines.append("inside")
        elif self.first_location > INSIDE_LINE: # 오른쪽에서 처음 감지되었을 때
            if center_x > INSIDE_LINE and "inside" not in self.passed_lines:
                self.passed_lines.append("inside")
            elif center_x < OUTSIDE_LINE and "outside" not in self.passed_lines:
                self.passed_lines.append("outside")

        # 두 개의 기록이 존재하면 방향 판별
        if len(self.passed_lines) >= 2:
            if self.passed_lines == ["inside", "outside"]:
                self.direction = "exit" # 안 -> 바깥 = 퇴장
            elif self.passed_lines == ["outside", "inside"]:
                self.direction = "entry" # 바깥 -> 안 = 입장

# 모든 사람 객체 저장 (track_id 기준)
persons = {}

# 이동 방향에 따라 저장할 이미지 리스트
exit_persons = []
entry_persons = []

def apply_mosaic_to_head(image, xmin, ymin, xmax, ymax, mosaic_ratio=0.1):
    """ 사람 바운딩 박스의 상단을 머리로 간주하고 모자이크 처리 """
    head_height = int((ymax - ymin) * 0.3)  # 상단 30%를 머리로 간주
    head_ymax = ymin + head_height

    head_region = image[ymin:head_ymax, xmin:xmax]
    if head_region.size == 0:
        return image  # 잘못된 영역 방지

    # 모자이크 효과 적용
    small = cv2.resize(head_region, (max(1, int((xmax - xmin) * mosaic_ratio)), max(1, int(head_height * mosaic_ratio))), interpolation=cv2.INTER_LINEAR)
    mosaic = cv2.resize(small, (xmax - xmin, head_height), interpolation=cv2.INTER_NEAREST)

    image[ymin:head_ymax, xmin:xmax] = mosaic
    return image

@app.get("/run-yolo")
def process_video():
    global OUTSIDE_LINE, INSIDE_LINE, persons, exit_persons, entry_persons

    video_cap = cv2.VideoCapture("test_video3.mp4")

    frame_count = 0

    # 첫 번째 프레임에서 영상 크기 확인하여 선 위치 설정
    ret, frame = video_cap.read()
    if not ret:
        return {"status": "Error: 영상 파일을 읽을 수 없습니다."}

    frame_width = frame.shape[1]
    OUTSIDE_LINE = frame_width // 3       # 1/3 지점
    INSIDE_LINE = (frame_width * 2) // 3     # 2/3 지점

    while True:
        start = datetime.datetime.now() # FPS 측정을 위한 시간
        ret, frame = video_cap.read()
        if not ret:
            break

        frame_count += 1

        results = model(frame)[0]
        detections = [] # 사람 감지를 위한 리스트트
        detected_items = []  # 소지품 감지를 위한 리스트
        
        for data in results.boxes.data.tolist():
            xmin, ymin, xmax, ymax, confidence, class_id = data
            if confidence < CONFIDENCE_THRESHOLD:
                continue
            class_name = results.names[class_id]
            
            width, height = xmax - xmin, ymax - ymin
            bbox = [xmin, ymin, width, height]
            
            if class_name == "person":
                detections.append((bbox, confidence, class_id))
            else:
                detected_items.append((class_name, bbox))  # 소지품 저장

        tracks = tracker.update_tracks(detections, frame=frame)

        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            xmin, ymin, xmax, ymax = map(int, track.to_ltrb())
            center_x = (xmin + xmax) // 2

            if track_id not in persons:
                persons[track_id] = Person(track_id, center_x)

            person = persons[track_id]
            person.update_position(center_x)
            
            # **사람과 겹치는 소지품 저장**
            for item_name, (ixmin, iymin, ixmax, iymax) in detected_items:
                person.items.add(item_name)  # 소지품 추가
                # if (xmin < ixmin < xmax and ymin < iymin < ymax) or (xmin < ixmax < xmax and ymin < iymax < ymax):
                #     person.items.add(item_name)  # 소지품 추가

            # 이동 방향이 특정된 경우, 모자이크 처리 후 이미지 저장
            if person.direction and person.direction not in person.passed_lines:
                frame_copy = frame.copy()

                # 얼굴 감지 및 모자이크 처리
                gray_frame = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                
                frame_copy = apply_mosaic_to_head(frame_copy, xmin, ymin, xmax, ymax)
                # 바운딩 박스 영역만 크롭 후 저장
                person_crop = frame_copy[ymin:ymax, xmin:xmax]  # 바운딩 박스 영역 자르기
                
                if person_crop.size != 0: # 빈 이미지 방지
                    filename = f"{person.direction}_{track_id}.jpg"
                    cv2.imwrite(f"images/{filename}", person_crop)

                if person.direction == "exit":
                    exit_persons.append({"image": filename, "items": list(person.items)})
                else:
                    entry_persons.append({"image": filename, "items": list(person.items)})

                person.passed_lines.append(person.direction) 

            # Bounding Box 그리기
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
            cv2.putText(frame, f"{track_id} - person", (xmin + 5, ymin - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)

        # 🔥 두 개의 가상의 선을 영상에 표시 (입구/출구 라벨 추가)
        cv2.line(frame, (OUTSIDE_LINE, 0), (OUTSIDE_LINE, frame.shape[0]), RED, 2)
        cv2.putText(frame, "outside line", (OUTSIDE_LINE - 40, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, RED, 2)

        cv2.line(frame, (INSIDE_LINE, 0), (INSIDE_LINE, frame.shape[0]), RED, 2)
        cv2.putText(frame, "inside line", (INSIDE_LINE - 20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, RED, 2)
        
        
        end = datetime.datetime.now()
        fps = f"FPS: {1 / (end - start).total_seconds():.2f}"
        cv2.putText(frame, fps, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 8)
        
        cv2.imshow("YOLO Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    video_cap.release()
    cv2.destroyAllWindows()

    return {
        "status": "YOLO 실행 완료",
        "entry_person": entry_persons,
        "exit_person": exit_persons
    }


# FastAPI에 정적 파일 서빙 설정
app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")

@app.get("/get-images")
def get_images():
    """ 저장된 입출입 이미지 목록과 소지품 정보를 제공하는 API """
    return {
        "entry_persons": [
            {"image": f"http://127.0.0.1:8000/images/{person['image']}", "items": person["items"]}
            for person in entry_persons
        ],
        "exit_persons": [
            {"image": f"http://127.0.0.1:8000/images/{person['image']}", "items": person["items"]}
            for person in exit_persons
        ]
    }

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
