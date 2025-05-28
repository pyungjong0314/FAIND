from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import router
from websocket_handler import ws_router
from admin_router import router as admin_router

app = FastAPI(title="YOLO Door Server")

app.include_router(router)
app.include_router(ws_router)
app.include_router(admin_router)
app.mount("/images", StaticFiles(directory="images"), name="images")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
