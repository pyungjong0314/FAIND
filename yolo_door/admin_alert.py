from fastapi import WebSocket
from websocket_handler import ws_router
from typing import List

connected_admins: List[WebSocket] = []


async def register_admin(ws: WebSocket):
    await ws.accept()
    connected_admins.append(ws)


async def unregister_admin(ws: WebSocket):
    if ws in connected_admins:
        connected_admins.remove(ws)


async def send_alert(message: str):
    for ws in connected_admins:
        try:
            await ws.send_text(message)
        except:
            await unregister_admin(ws)


@ws_router.websocket("/ws/admin-alert")
async def alert_websocket(ws: WebSocket):
    await register_admin(ws)
    try:
        while True:
            await ws.receive_text()
    except:
        await unregister_admin(ws)
