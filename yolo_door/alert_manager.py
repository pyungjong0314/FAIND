# alert_manager.py

from datetime import datetime
from typing import List
import asyncio

from admin_alert import send_alert


def notify_admin_lost_items(timestamp: datetime, location: str, missing_items: List[str]):
    # 분실물이 감지되었을 때 관리자 웹에만 WebSocket 알림을 전송하는 함수

    alert_msg = f"[ALERT] {timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {location} | 분실물: {', '.join(missing_items)}"

    try:
        # 이미 비동기 환경이라면 바로 task로 실행
        asyncio.create_task(send_alert(alert_msg))
        print("[AlertManager] WebSocket 관리자 알림 전송 완료")
    except RuntimeError:
        # 동기 환경에서 fallback 처리
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_alert(alert_msg))
        loop.close()
        print("[AlertManager] WebSocket 관리자 알림 전송 완료 (new loop)")
