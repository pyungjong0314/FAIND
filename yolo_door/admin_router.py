from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/admin", response_class=HTMLResponse)
def admin_page():
    return """
    <html>
        <head><title>관리자 알림 페이지</title></head>
        <body>
            <h2>📢 분실물 감지 알림</h2>
            <ul id="alerts"></ul>

            <script>
                const alerts = document.getElementById("alerts");
                const socket = new WebSocket("ws://" + location.host + "/ws/admin-alert");

                socket.onmessage = function(event) {
                    const li = document.createElement("li");
                    li.innerText = event.data;
                    alerts.prepend(li);  // 최신 알림이 위로
                };
            </script>
        </body>
    </html>
    """
