# app/models/financial_product.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class FinancialProducts(Base):
    __tablename__ = "financial_products"

    financial_product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    ticker = Column(String(20), nullable=False, unique=True)

    sector_id = Column(Integer, ForeignKey("sectors.sector_id"), nullable=False)
    sector = relationship("Sectors", back_populates="financial_products")
