from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import router
from websocket_handler import ws_router
from admin_router import router as admin_router

app = FastAPI(title="YOLO Door Server")

# CORS 설정 (아주 중요!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*"은 모든 출처 허용. 실제 서비스에서는 도메인 지정 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(ws_router)
app.include_router(admin_router)
app.mount("/images", StaticFiles(directory="images"), name="images")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
