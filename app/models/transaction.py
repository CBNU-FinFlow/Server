# app/models/transaction.py

from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class TransactionHistory(Base):
    __tablename__ = "transaction_history"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_id = Column(
        Integer, ForeignKey("portfolios.portfolio_id"), nullable=False
    )
    financial_product_id = Column(
        Integer, ForeignKey("financial_products.financial_product_id"), nullable=False
    )
    transaction_type = Column(String(50), nullable=False)
    price = Column(Numeric(18, 2), nullable=False)
    profit_rate = Column(Numeric(5, 2))
    currency_code = Column(String(10))
    quantity = Column(Numeric(18, 4))
    created_at = Column(DateTime)

    # 관계 설정
    portfolio = relationship("Portfolio", back_populates="transactions")
    financial_product = relationship("FinancialProducts", back_populates="transactions")
