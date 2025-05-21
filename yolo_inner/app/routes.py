from fastapi import APIRouter
from processor_adapter import get_lost_json, run_test_video

router = APIRouter()


@router.get("/get-lost")
def get_lost_items():
    return get_lost_json()


@router.get("/run-test")
def run_test():
    run_test_video()
    return {"status": "Test inference completed."}
