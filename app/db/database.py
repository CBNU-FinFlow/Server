# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


# MySQL 사용
engine = create_engine(
    settings.DB_URL,
    echo=False,  # 로그 출력 여부 (개발 환경에서 True 권장)
    pool_pre_ping=True  # MySQL 커넥션 유효성 체크 (옵션)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()