# app/models/asset.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.database import Base


class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.uid"), nullable=False)  # 유저 ID
    asset_name = Column(String(100), nullable=False)  # 자산 이름 (예: 삼성전자 주식)
    asset_type = Column(
        String(50), nullable=False
    )  # 자산 유형 (예: 주식, 펀드, 채권 등)
    quantity = Column(Float, nullable=False)  # 보유 수량
    purchase_price = Column(Float, nullable=False)  # 매입 단가
    current_value = Column(Float, nullable=True)  # 현재 평가 금액

    owner = relationship("User", back_populates="assets")  # 유저와의 관계
