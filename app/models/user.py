# app/models/user.py
from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    investment_profile = Column(String(100), nullable=True)
    profile_image = Column(String(255), nullable=True)

    assets = relationship("Asset", back_populates="owner", cascade="all, delete-orphan")
    accounts = relationship(
        "Account", back_populates="user", cascade="all, delete-orphan"
    )
