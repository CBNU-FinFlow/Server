# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine

# 모든 모델을 명시적으로 import 하여 등록
from app.models import user
from app.models import portfolio
from app.models import financial_product
from app.models import sector

from app.routers import users
from app.routers import assets

# DB 생성 전에 모든 모델이 등록되어야 합니다.
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용 (프로덕션에서는 구체적인 도메인 지정 권장)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 라우터 등록
app.include_router(users.router)
app.include_router(assets.router)
