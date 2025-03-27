import cv2
import datetime
import numpy as np
import os
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from db import insert_capture_info

model = YOLO("yolo11n.pt")
tracker = DeepSort(max_age=50)
CONFIDENCE_THRESHOLD = 0.8
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

OUTSIDE_LINE = None
INSIDE_LINE = None
persons = {}
entry_persons = []
exit_persons = []


class Person:
    def __init__(self, track_id, first_location):
        self.track_id = track_id
        self.passed_lines = []
        self.direction = None
        self.first_location = first_location
        self.items = set()

    def update_position(self, center_x):
        if self.first_location < OUTSIDE_LINE:
            if center_x > OUTSIDE_LINE and "outside" not in self.passed_lines:
                self.passed_lines.append("outside")
            elif center_x > INSIDE_LINE and "inside" not in self.passed_lines:
                self.passed_lines.append("inside")
        elif self.first_location > INSIDE_LINE:
            if center_x > INSIDE_LINE and "inside" not in self.passed_lines:
                self.passed_lines.append("inside")
            elif center_x < OUTSIDE_LINE and "outside" not in self.passed_lines:
                self.passed_lines.append("outside")

        if len(self.passed_lines) >= 2:
            if self.passed_lines == ["inside", "outside"]:
                self.direction = "exit"
            elif self.passed_lines == ["outside", "inside"]:
                self.direction = "entry"


def apply_mosaic_to_head(image, xmin, ymin, xmax, ymax, mosaic_ratio=0.1):
    head_height = int((ymax - ymin) * 0.3)
    head_ymax = ymin + head_height
    head_region = image[ymin:head_ymax, xmin:xmax]
    if head_region.size == 0:
        return image
    small = cv2.resize(head_region, (max(1, int((xmax - xmin) * mosaic_ratio)),
                       max(1, int(head_height * mosaic_ratio))), interpolation=cv2.INTER_LINEAR)
    mosaic = cv2.resize(small, (xmax - xmin, head_height),
                        interpolation=cv2.INTER_NEAREST)
    image[ymin:head_ymax, xmin:xmax] = mosaic
    return image


def run_yolo_on_frame(frame):
    global OUTSIDE_LINE, INSIDE_LINE, persons, entry_persons, exit_persons

    if OUTSIDE_LINE is None or INSIDE_LINE is None:
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
        width, height = xmax - xmin, ymax - ymin
        bbox = [xmin, ymin, width, height]

        if class_name == "person":
            detections.append((bbox, confidence, class_id))
        else:
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

        for item_name, (ixmin, iymin, ixmax, iymax) in detected_items:
            if (xmin < ixmin < xmax and ymin < iymin < ymax) or (xmin < ixmax < xmax and ymin < iymax < ymax):
                person.items.add(item_name)

        if person.direction and person.direction not in person.passed_lines:
            frame_copy = frame.copy()
            frame_copy = apply_mosaic_to_head(
                frame_copy, xmin, ymin, xmax, ymax)
            person_crop = frame_copy[ymin:ymax, xmin:xmax]
            if person_crop.size != 0:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{person.direction}_{timestamp}.jpg"
                filepath = os.path.join(IMAGE_DIR, filename)
                cv2.imwrite(filepath, person_crop)
                insert_capture_info(filename, filepath)
                info = {"image": filename, "items": list(person.items)}
                if person.direction == "entry":
                    entry_persons.append(info)
                else:
                    exit_persons.append(info)
            person.passed_lines.append(person.direction)

    cv2.imshow("Live Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
