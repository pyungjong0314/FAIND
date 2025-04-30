from fastapi import FastAPI, Header, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional
import httpx
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

# .env 파일 로드
load_dotenv()

# 환경변수에서 관리자 토큰 불러오기
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

# 이미지 디렉토리 마운트
IMAGE_DIR = "/app/saved_people"
os.makedirs(IMAGE_DIR, exist_ok=True)


app = FastAPI()

# URL 경로 "/images"로 정적 이미지 서비스 제공
app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")

# 관리자 인증 함수


def verify_admin(token: Optional[str]):
    if token != ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

# 감지 결과 조회 API (공개)


@app.get("/api/detections")
async def get_detections():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://main_server:8000/get-detections?limit=10")
            return JSONResponse(content=response.json())
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# 감지 결과 삭제 API (관리자만)


@app.delete("/api/delete/{detection_id}")
async def delete_detection(detection_id: int, x_admin_token: Optional[str] = Header(None)):
    verify_admin(x_admin_token)
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"http://main_server:8000/delete-detection/{detection_id}")
        return response.json()

# 감지 결과 상태 업데이트 API (관리자만)


@app.put("/api/update-status/{detection_id}")
async def update_status(detection_id: int, new_status: str, x_admin_token: Optional[str] = Header(None)):
    verify_admin(x_admin_token)
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"http://main_server:8000/update-status/{detection_id}",
            params={"new_status": new_status}
        )
        return response.json()
