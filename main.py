from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import router
from config import IMAGE_DIR

app = FastAPI()

# API 라우터 등록
app.include_router(router)

# 정적 파일 서빙
app.mount("/../images", StaticFiles(directory=IMAGE_DIR), name="images")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

