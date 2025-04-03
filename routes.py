from fastapi import APIRouter
from video_processor import process_video, entry_persons, exit_persons
from config import IMAGE_DIR

router = APIRouter()

@router.get("/run-yolo")
def run_yolo():
    return process_video()

@router.get("/get-images")
def get_images():
    return {
        "entry_persons": [
            {"image": f"/images/{person['image']}", "items": person["items"]}
            for person in entry_persons
        ],
        "exit_persons": [
            {"image": f"/images/{person['image']}", "items": person["items"]}
            for person in exit_persons
        ]
    }
