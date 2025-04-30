import psycopg2
from typing import Optional
from datetime import datetime

# PostgreSQL에 연결하는 함수


def connect_db():
    conn = psycopg2.connect(
        dbname="video_db",         # 데이터베이스 이름
        user="video_user",         # 사용자명
        password="video_pass",     # 비밀번호
        host="postgres_db",        # docker-compose에서 정의한 DB 서비스 이름
        port="5432"                # PostgreSQL 기본 포트
    )
    return conn

# 감지 테이블 생성 (처음 실행 시)


def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id SERIAL PRIMARY KEY,              -- 감지 결과 고유 ID
            label TEXT,                         -- 객체 이름
            confidence FLOAT,                   -- 신뢰도
            x1 INT, y1 INT, x2 INT, y2 INT,     -- 바운딩 박스 좌표
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 생성 시간
            status TEXT DEFAULT 'pending',      -- 처리 상태 (기본값: pending)
            image_path TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# 감지 결과를 DB에 삽입


def insert_detection(label: str, confidence: float, bbox: list, image_path: Optional[str] = None):
    x1, y1, x2, y2 = bbox
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO detections (label, confidence, x1, y1, x2, y2, image_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (label, confidence, x1, y1, x2, y2, image_path))
    conn.commit()
    cur.close()
    conn.close()


# 감지 결과 조회 함수


def get_detections(limit=10, label: Optional[str] = None,
                   start_time: Optional[datetime] = None,
                   end_time: Optional[datetime] = None):
    conn = connect_db()
    cur = conn.cursor()

    query = """
        SELECT label, confidence, x1, y1, x2, y2, timestamp, status
        FROM detections
        WHERE 1=1
    """
    params = []

    if label:
        query += " AND label = %s"
        params.append(label)
    if start_time:
        query += " AND timestamp >= %s"
        params.append(start_time)
    if end_time:
        query += " AND timestamp <= %s"
        params.append(end_time)

    query += " ORDER BY timestamp DESC LIMIT %s"
    params.append(limit)

    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "label": row[0],
            "confidence": row[1],
            "bbox": [row[2], row[3], row[4], row[5]],
            "timestamp": row[6].isoformat(),
            "status": row[7]
        })

    return result

# 감지 결과 삭제 (ID 기준)


def delete_detection_by_id(detection_id: int):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM detections WHERE id = %s", (detection_id,))
    conn.commit()
    cur.close()
    conn.close()

# 감지 결과 상태 업데이트


def update_detection_status(detection_id: int, new_status: str):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE detections SET status = %s WHERE id = %s",
                (new_status, detection_id))
    conn.commit()
    cur.close()
    conn.close()
