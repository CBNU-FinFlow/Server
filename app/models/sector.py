# app/models/sector.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Sectors(Base):
    __tablename__ = "sectors"

    sector_id = Column(Integer, primary_key=True, index=True)
    sector_name = Column(String(100), nullable=False, unique=True)

    financial_products = relationship("FinancialProducts", back_populates="sector")
