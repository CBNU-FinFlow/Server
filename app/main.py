# app/main.py
from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import users
from app.models import user as user_model

# DB 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 라우터 등록
app.include_router(users.router)