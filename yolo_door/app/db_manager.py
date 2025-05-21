from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
from sqlalchemy.sql import text
from datetime import datetime
import os
from dotenv import load_dotenv
import numpy as np
from utils import extract_feature_vector, compute_cosine_similarity

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class PersonEntry(Base):
    __tablename__ = "person_entries"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, nullable=False)
    direction = Column(String, nullable=False)
    feature_vector = Column(Vector(512))
    image_path = Column(String)
    items = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)


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


def find_matching_person(feature_vector, threshold=0.75):
    session = SessionLocal()
    all_entries = session.query(PersonEntry).filter(
        PersonEntry.direction == "entry").all()

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
        print(
            f"[DB] Found matching entry ID: {matched_entry.id} with sim={max_sim:.3f}")
        return matched_entry
    else:
        print("[DB] No matching entry found.")
        return None


def compare_items(entry_items, exit_items):
    missing_items = list(set(entry_items) - set(exit_items))
    print(f"[COMPARE] Missing items: {missing_items}")
    return missing_items


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("[DB] person_entries 테이블 초기화 완료")
