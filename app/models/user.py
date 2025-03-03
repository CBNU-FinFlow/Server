# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    investment_profile = Column(String(100), nullable=True)
    profile_image = Column(String(255), nullable=True)

    # 새로 추가 또는 수정: Portfolio 모델과 1:N 관계
    portfolios = relationship("Portfolio", back_populates="user")
