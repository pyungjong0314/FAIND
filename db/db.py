from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

# 📌 DB 연결 정보 수정하기기
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/yolo_project"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Capture(Base):
    __tablename__ = "captures"
    filename = Column(String(255), primary_key=True)
    path = Column(String(255))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


# DB에 테이블 생성 (없을 시 자동 생성)
Base.metadata.create_all(bind=engine)


def insert_capture_info(filename: str, path: str):
    db = SessionLocal()
    capture = Capture(filename=filename, path=path)
    db.add(capture)
    db.commit()
    db.close()
