from fastapi import FastAPI
from routes import router
from websocket_handler import ws_router

app = FastAPI(title="YOLO Inner Server")

app.include_router(router)
app.include_router(ws_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
