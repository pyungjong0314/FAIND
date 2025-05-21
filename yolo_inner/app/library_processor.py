import cv2
import time
from datetime import datetime
from ultralytics import YOLO
import json


class TrackedObject:
    def __init__(self, object_id, class_name, last_position):
        self.object_id = object_id
        self.class_name = class_name
        self.having = True
        self.timestamp = None
        self.count = 0
        self.last_position = last_position

    def update_having(self, has_person_near):
        if has_person_near:
            self.having = True
            self.timestamp = None
        else:
            if self.having:
                self.timestamp = datetime.now()
            self.having = False


def calculate_distance(box1, box2):
    x1_center = (box1[0] + box1[2]) / 2
    y1_center = (box1[1] + box1[3]) / 2
    x2_center = (box2[0] + box2[2]) / 2
    y2_center = (box2[1] + box2[3]) / 2
    return ((x1_center - x2_center) ** 2 + (y1_center - y2_center) ** 2) ** 0.5

def get_lost_objects_json():
    return json.dumps([
        {
            "track_id": obj.object_id,
            "class": obj.class_name,
            "lost_time": obj.timestamp.strftime("%Y-%m-%d %H:%M:%S") if obj.timestamp else None
        }
        for obj in lost_objects.values()
    ], indent=4)



model = YOLO("yolov8x.pt")
video_source = "library3.mp4"
cap = cv2.VideoCapture(video_source)

threshold_distance = 380
frame_interval = 5
candidate_check_interval = 5  # 10분

last_detection_time = None
last_candidate_check = datetime.now()

non_objects = ["bench", "dining table", "chair", "tv", "remote", "keyboard"]

tracked_objects = {}
candidate_objects = {}
lost_objects = {}
latest_tracked_boxes = []  # 유지할 바운딩 박스 저장용



def run_inference(frame):
    global tracked_objects, candidate_objects, lost_objects, last_detection_time, latest_tracked_boxes

    last_detection_time = datetime.now()
    results = model.track(frame, persist=True)[0]
    boxes = results.boxes
    latest_tracked_boxes = [box for box in boxes if results.names[int(box.cls[0])] not in non_objects]  # 유효 객체만 저장
    current_ids = set()

    people_boxes = []
    object_boxes = []

    for box in boxes:
        class_id = int(box.cls[0])
        class_name = results.names[class_id]
        if class_name in non_objects:
            continue

        track_id = int(box.id[0]) if box.id is not None else -1
        bbox = box.xyxy[0].tolist()
        x1, y1, x2, y2 = map(int, bbox)

        if class_name == "person":
            people_boxes.append(box)
        else:
            object_boxes.append(box)

        if track_id != -1:
            color = (0, 255, 0) if class_name == "person" else (0, 255, 255)
            label = f"{class_name}-{track_id}"
            if class_name != "person" and track_id in tracked_objects:
                obj = tracked_objects[track_id]
                label += f"-{'Having' if obj.having else 'Not Having'}"
                color = (0, 255, 255) if obj.having else (0, 0, 255)
            elif class_name != "person":
                label += "-Not Having"
                color = (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    for box in object_boxes:
        track_id = int(box.id[0])
        class_name = results.names[int(box.cls[0])]
        bbox = box.xyxy[0].tolist()
        current_ids.add(track_id)

        if track_id not in tracked_objects:
            tracked_objects[track_id] = TrackedObject(track_id, class_name, bbox)

        obj = tracked_objects[track_id]
        near_person = any(calculate_distance(bbox, p.xyxy[0].tolist()) < threshold_distance for p in people_boxes)
        obj.update_having(near_person)

    for tid in list(tracked_objects):
        if tid not in current_ids:
            tracked_objects.pop(tid, None)
            candidate_objects.pop(tid, None)

# -------------------------------
# 메인 루프
# -------------------------------
fps = cap.get(cv2.CAP_PROP_FPS)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    now = datetime.now()

    if last_detection_time is None or (now - last_detection_time).total_seconds() >= frame_interval:
        run_inference(frame)

    # 이전 프레임의 추적 결과 유지 시각화
    for box in latest_tracked_boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        if class_name in non_objects:
            continue

        track_id = int(box.id[0]) if box.id is not None else -1
        bbox = box.xyxy[0].tolist()
        x1, y1, x2, y2 = map(int, bbox)
        color = (0, 255, 0) if class_name == "person" else (0, 255, 255)
        label = f"{class_name}-{track_id}"
        if class_name != "person" and track_id in tracked_objects:
            obj = tracked_objects[track_id]
            label += f"-{'Having' if obj.having else 'Not Having'}"
            color = (0, 255, 255) if obj.having else (0, 0, 255)
        elif class_name != "person":
            label += "-Not Having"
            color = (0, 0, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # 10분마다 having 상태 확인
    if (now - last_candidate_check).total_seconds() >= candidate_check_interval:
        for tid, obj in list(candidate_objects.items()):
            if obj.having: # 다시 having 상태로 돌아가면 1씩 줄어듦
                obj.count = max(0, obj.count - 1)
                if obj.count == 0:
                    candidate_objects.pop(tid)
            
            else:
                obj.count += 1
                if obj.count >= 3:
                    lost_objects[tid] = obj
                    candidate_objects.pop(tid, None)

        for tid, obj in tracked_objects.items():
            if not obj.having and tid not in lost_objects:
                candidate_objects[tid] = obj

        last_candidate_check = now

    # 결과 출력
    cv2.imshow("Lost Item Detection", frame)
    if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# 결과 출력
print(get_lost_objects_json())