## 📦 기능 요약

- 실시간 영상 전송 (WebSocket)
- YOLOv5 기반 객체 감지
- 감지 결과 DB 저장 (PostgreSQL)
- 감지된 사람이면 이미지 저장 + DB에 경로 저장
- 관리자 기능 (삭제/상태 업데이트)
- 감지 이미지 웹에서 조회 가능 (`/images/...`)
- REST API 기반 조회 시스템

---

## 🗂️ 디렉토리 구조

```
FAIND/
├── docker-compose.yml
├── camera_client/
│   └── client.py
├── main_server/
│   ├── main.py
│   ├── db.py
│   └── requirements.txt
├── yolo_server/
│   ├── app/
│   │   ├── yolo_main.py
│   │   └── yolo_model.py
│   └── requirements.txt
├── web_server/
│   ├── web_main.py
│   ├── .env
│   └── requirements.txt
```

---

## 🧰 요구사항

- Docker + docker-compose
- 로컬 Linux 환경에서 `/dev/video0` 사용 가능해야 함

---

## 🚀 실행 방법

```bash
# 실행
docker-compose up --build
```

> 실행 후 주요 서비스는 다음과 같이 접근 가능합니다:

| 서비스 | 주소 |
|--------|------|
| WebSocket 수신 (main_server) | `ws://localhost:8000/ws/stream` |
| YOLO 추론 API (내부용) | `http://yolo_server:8001/predict` |
| 감지 결과 REST API | `http://localhost:8080/api/detections` |
| 감지 이미지 조회 | `http://localhost:8080/images/<filename>.jpg` |

---

## 🔐 관리자 기능 (인증 방식)

관리자 API를 호출할 때는 다음 헤더를 포함해야 합니다:

```http
X-Admin-Token: <your_token>
```

> 토큰은 `web_server/.env` 파일 내에 `ADMIN_TOKEN=...`으로 정의됨

---

## 📡 주요 API

### 감지 결과 조회
```http
GET /api/detections?limit=10&label=person&start_time=...&end_time=...
```

### 감지 결과 삭제
```http
DELETE /api/delete/{id}
Headers: X-Admin-Token: your_token
```

### 상태 업데이트
```http
PUT /api/update-status/{id}?new_status=processed
Headers: X-Admin-Token: your_token
```

---

## ⚠️ 주의사항

- 카메라 송신 클라이언트는 Docker에서 `--device=/dev/video0`로 장치 접근 허용해야 함
- `.env` 파일은 Git에 업로드하지 말고 로컬에서만 관리하세요
- PostgreSQL의 데이터는 volume으로 영속화됩니다 (`pgdata`)

---

## 📜 라이선스

MIT License
