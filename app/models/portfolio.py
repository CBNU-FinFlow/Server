from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

    portfolio_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.uid"), nullable=False)
    total_assets = Column(DECIMAL(18, 2), nullable=True)
    expected_dividend = Column(DECIMAL(18, 2), nullable=True)

