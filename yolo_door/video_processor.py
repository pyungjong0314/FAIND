import cv2
import datetime
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from utils import apply_mosaic_to_head, extract_feature_vector
from models import Person
from db_manager import save_entry_to_db, find_matching_person, compare_items
from notifier import post_item_to_main_server, send_faind_email
import os
import threading
import queue
from alert_manager import notify_admin_lost_items

# YOLO 모델 및 추적기 초기화
model = YOLO("yolov8n.pt")
tracker = DeepSort(max_age=50)

# 이동 방향 감지
persons = {}
exit_persons = []
entry_persons = []

CONFIDENCE_THRESHOLD = 0.45 # 기존 0.6에서 0.45로 변경
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (0, 0, 255)

os.makedirs("images", exist_ok=True)
os.makedirs("images/items", exist_ok=True)

desired_classes = ['backpack', 'umbrella'] # 확인하기 원하는 것들 명시

### 이메일을 위한 비밀번호 입력
PASSWORD = ""

# 최대 프레임 버퍼 : 30개
frame_queue = queue.Queue(maxsize=30)


def frame_consumer():
    while True:
        try:
            while frame_queue.qsize() > 1:
                frame_queue.get()
            frame = frame_queue.get()
            process_frame(frame)
        except Exception as e:
            print(f"[Frame Processor] 오류 발생: {e}")


def start_frame_processor():
    thread = threading.Thread(target=frame_consumer, daemon=True)
    thread.start()


# 스레드 실행
start_frame_processor()


def process_test_by_video():  # 영상으로 테스트하는 버전
    video_cap = cv2.VideoCapture("test_video2.mp4")
    ret, frame = video_cap.read()
    if not ret:
        return {"status": "Error: 영상 파일을 읽을 수 없습니다."}

    while True:
        ret, frame = video_cap.read()
        if not ret:
            break
        process_frame(frame)
    video_cap.release()
    cv2.destroyAllWindows()
    return {
        "status": "YOLO 실행 완료",
        "entry_person": entry_persons,
        "exit_person": exit_persons
    }


def process_frame(frame):
    global OUTSIDE_LINE, INSIDE_LINE, persons, exit_persons, entry_persons

    frame_width = frame.shape[1]
    OUTSIDE_LINE = frame_width // 3
    INSIDE_LINE = (frame_width * 2) // 3

    results = model(frame)[0]
    detections = []
    detected_items = []

    for data in results.boxes.data.tolist():
        xmin, ymin, xmax, ymax, confidence, class_id = data
        if confidence < CONFIDENCE_THRESHOLD:
            continue
        class_name = results.names[class_id]
        width = xmax - xmin
        height = ymax - ymin
        bbox = [xmin, ymin, width, height]
        if class_name == "person":
            detections.append((bbox, confidence, class_id))
        elif class_name in desired_classes:
            detected_items.append((class_name, bbox))

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
        person.update_position(center_x)  # line 넘었는지 확인하고 방향 판정.

        for item_name, (ixmin, iymin, iwidth, iheight) in detected_items:
            ixmax = ixmin + iwidth
            iymax = iymin + iheight
            item_center_x = (ixmin + ixmax) // 2

            if OUTSIDE_LINE <= item_center_x <= INSIDE_LINE:
                if item_name not in person.items:
                    person.items[item_name] = (ixmin, iymin, ixmax, iymax)
                    item_crop = frame[int(iymin):int(
                        iymax), int(ixmin):int(ixmax)]
                    if item_crop.size != 0:
                        item_filename = f"{track_id}_{item_name}.jpg"
                        cv2.imwrite(f"images/items/{item_filename}", item_crop)

        if person.direction and person.direction not in person.passed_lines:
            frame_copy = frame.copy()
            person_crop = frame_copy[ymin:ymax, xmin:xmax]
            if person_crop.size == 0:
                continue
            person.feature_vector = extract_feature_vector(person_crop)
            frame_copy = apply_mosaic_to_head(
                frame_copy, xmin, ymin, xmax, ymax)
            filename = f"{person.direction}_{track_id}.jpg"
            save_path = os.path.abspath(f"images/{filename}")
            cv2.imwrite(save_path, frame_copy[ymin:ymax, xmin:xmax])
            item_names = list(person.items.keys())
            if person.direction == "entry":
                save_entry_to_db(track_id, person.direction,
                                 person.feature_vector, save_path, item_names)
                entry_persons.append({"image": filename, "items": item_names})
            elif person.direction == "exit":  # 나가는 사람 발생시 비교.
                matched_entry = find_matching_person(person.feature_vector)
                if matched_entry:
                    missing_items = compare_items(matched_entry.items, item_names)
                    print(f"[ALERT] Person {matched_entry.id} missing: {missing_items}")
                    if missing_items:
                        notify_admin_lost_items(datetime.now(), "도서관 내부 어딘가", missing_items)
                        post_item_to_main_server(datetime.now(), "도서관 내부 어딘가", missing_items)
                        send_faind_email(
                            subject="FAIND - 분실물 감지 알림",
                            item_name=missing_items,
                            location="도서관 내부",
                            timestamp=datetime.datetime.now(),
                            to_email = "sonopj@kw.ac.kr",
                            from_email = "2025kwchambit@gmail.com",
                            from_password = PASSWORD
                        )
                else:
                    print("일치하는 사람이 없다? 이상하다?")
            person.passed_lines.append(person.direction)

        # Bounding Box 그리기
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
        cv2.putText(frame, f"{track_id} - person", (xmin + 5, ymin - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
        
        # 각 사람의 소지품 bbox 그리기
        for item_name, (ixmin, iymin, ixmax, iymax) in person.items.items():
            cv2.rectangle(frame, (int(ixmin), int(iymin)), (int(ixmax), int(iymax)), RED, 2)
            cv2.putText(frame, f"{track_id} - {item_name}", (int(ixmin) + 5, int(iymin) - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)

    # 두 개의 가상의 선을 영상에 표시 (입구/출구 라벨 추가)
    cv2.line(frame, (OUTSIDE_LINE, 0), (OUTSIDE_LINE, frame.shape[0]), RED, 2)
    cv2.putText(frame, "outside line", (OUTSIDE_LINE - 40, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, RED, 2)

    cv2.line(frame, (INSIDE_LINE, 0), (INSIDE_LINE, frame.shape[0]), RED, 2)
    cv2.putText(frame, "inside line", (INSIDE_LINE - 20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, RED, 2)
    
    # resize 필요시 사용
    # frame_resized = cv2.resize(frame, (width, height))
    # cv2.imshow("YOLO Tracking", frame_resized)
    
    cv2.imshow("YOLO Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
