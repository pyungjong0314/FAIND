import cv2
import datetime
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from config import YOLO_MODEL_PATH, CONFIDENCE_THRESHOLD, OUTSIDE_LINE, INSIDE_LINE
from utils import apply_mosaic_to_head
from models import Person
import os

# YOLO 모델 및 추적기 초기화
model = YOLO(YOLO_MODEL_PATH)
tracker = DeepSort(max_age=50)

# 얼굴 검출기 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# 이동 방향 감지
persons = {}
exit_persons = []
entry_persons = []

CONFIDENCE_THRESHOLD = 0.6
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (0, 0, 255)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

def process_video(video_path=os.path.join(PROJECT_DIR, "test_video3.mp4")):
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
