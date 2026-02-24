import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# For production, we use PostgreSQL from Docker (Phase 7 upgrade)
# For local dev fallback without docker, default to sqlite
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_guitar_pedal.db")

# connect_args is only for sqlite
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
