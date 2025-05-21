import cv2
import datetime
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from utils import apply_mosaic_to_head, extract_feature_vector
from models import Person
from db_manager import save_entry_to_db, find_matching_person, compare_items
from notifier import send_alert_to_main_server
import os

# YOLO 모델 및 추적기 초기화
model = YOLO("yolov8n.pt")
tracker = DeepSort(max_age=50)

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

os.makedirs("images", exist_ok=True)
os.makedirs("images/items", exist_ok=True)

desired_classes = ['backpack', 'umbrella']


def is_overlapping(box1, box2):
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2
    return not (x1_max < x2_min or x2_max < x1_min or y1_max < y2_min or y2_max < y1_min)


def process_test_by_video():  # 영상으로 테스트하는 버전
    video_cap = cv2.VideoCapture("test_video5.mp4")
    ret, frame = video_cap.read()
    if not ret:
        return {"status": "Error: 영상 파일을 읽을 수 없습니다."}
    frame_width = frame.shape[1]
    OUTSIDE_LINE = frame_width // 3
    INSIDE_LINE = (frame_width * 2) // 3

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

    if 'OUTSIDE_LINE' not in globals() or 'INSIDE_LINE' not in globals():
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
        person.update_position(center_x)

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
                save_entry_to_db(track_id, "entry",
                                 person.feature_vector, save_path, item_names)
                entry_persons.append({"image": filename, "items": item_names})
            elif person.direction == "exit":
                matched_entry = find_matching_person(person.feature_vector)
                if matched_entry:
                    missing_items = compare_items(
                        matched_entry.items, item_names)
                    print(
                        f"[ALERT] Person {matched_entry.id} missing: {missing_items}")
                    if missing_items:
                        send_alert_to_main_server(
                            matched_entry.id, missing_items)
                    exit_persons.append(
                        {"image": filename, "items": item_names, "missing": missing_items})
                else:
                    exit_persons.append(
                        {"image": filename, "items": item_names})
            person.passed_lines.append(person.direction)

    cv2.imshow("YOLO Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
