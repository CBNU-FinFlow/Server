# app/models/user.py
from sqlalchemy import Column, Integer, String , DateTime
from sqlalchemy.sql import func 
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    investment_profile = Column(String(100), nullable=True)
    profile_image = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())