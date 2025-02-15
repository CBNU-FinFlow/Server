# app/models/account.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.database import Base


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.uid"), nullable=False)
    account_name = Column(String(100), nullable=False)
    balance = Column(Float, nullable=False)

    assets = relationship("Asset", back_populates="account")  # 계좌와 보유 자산 연결
