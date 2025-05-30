from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
from sqlalchemy.sql import text
from datetime import datetime
import numpy as np
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from utils import extract_feature_vector, compute_cosine_similarity

# 슈퍼유저 계정으로 설정
DB_HOST = "host.docker.internal" # 로컬에서 돌릴 때는 localhost로 변경.
DB_PORT = "5432"
DB_NAME = "yolo_db"
DB_USER = "postgres"
DB_PASSWORD = "0000"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# DB가 없으면 생성
def create_database_if_not_exists():
    try:
        con = psycopg2.connect(dbname='postgres', user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"[INIT] 데이터베이스 '{DB_NAME}' 생성 완료")
        else:
            print(f"[INIT] 데이터베이스 '{DB_NAME}' 이미 존재")

        cur.close()
        con.close()
    except Exception as e:
        print(f"[ERROR] DB 생성 오류: {e}")

# SQLAlchemy 세팅
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 테이블 정의
class PersonEntry(Base):
    __tablename__ = "person_entries"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, nullable=False)
    direction = Column(String, nullable=False)
    feature_vector = Column(Vector(512))
    image_path = Column(String)
    items = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

# 입장하는 사람 저장
def save_entry_to_db(track_id, direction, feature_vector, image_path, items):
    session = SessionLocal()
    person = PersonEntry(
        track_id=track_id,
        direction=direction,
        feature_vector=feature_vector,
        image_path=image_path,
        items=items,
    )
    session.add(person)
    session.commit()
    session.close()
    print(f"[DB] Saved person {track_id} ({direction})")

# 벡터 계산으로 유사한 사람 탐색
# feature_vector : 퇴장하는 사람의 벡터
# entry.feature_vector : 입장했던 사람들의 벡터
def find_matching_person(feature_vector, threshold=0.5):
    session = SessionLocal()
    all_entries = session.query(PersonEntry).filter(PersonEntry.direction == "entry").all()

    max_sim = -1
    matched_entry = None

    for entry in all_entries:
        if entry.feature_vector is None:
            continue
        sim = compute_cosine_similarity(feature_vector, entry.feature_vector)
        if sim > max_sim and sim >= threshold:
            max_sim = sim
            matched_entry = entry

    session.close()
    if matched_entry:
        print(f"[DB] Found matching entry ID: {matched_entry.id} with sim={max_sim:.3f}")
        return matched_entry
    else:
        print("[DB] No matching entry found.")
        return None

# 아이템 비교
def compare_items(entry_items, exit_items):
    missing_items = list(set(entry_items) - set(exit_items))
    print(f"[COMPARE] Missing items: {missing_items}")
    return missing_items

# 테이블 초기화
def init_db():
    Base.metadata.create_all(bind=engine)


# pgvector 확장 설치 확인.
def ensure_pgvector_extension():
    try:
        import psycopg2
        con = psycopg2.connect(
            dbname='yolo_db', user='postgres', password='0000',
            host='localhost', port='5432'
        )
        cur = con.cursor()
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        con.commit()
        cur.close()
        con.close()
        print("[DB] pgvector 확장 확인 완료")
    except Exception as e:
        print(f"[DB] pgvector 설치 오류: {e}")

# 실행
if __name__ == "__main__":
    create_database_if_not_exists()     # 1. DB 생성
    ensure_pgvector_extension()         # 2. pgvector 확장 확인
    init_db()                           # 3. 테이블 생성 (Vector 필드 포함)
    print("[DB] person_entries 테이블 초기화 완료")
