from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship 
from app.db.database import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

    portfolio_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    portfolio_name = Column(String(255), nullable = False)
    user_id = Column(Integer, ForeignKey("users.uid"), nullable=False)


    transactions = relationship("TransactionHistory", back_populates="portfolio")

