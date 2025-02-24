# app/models/portfolio.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime

from sqlalchemy.orm import relationship
from app.db.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    portfolio_id = Column(Integer, primary_key=True, index=True)
    portfolio_name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.uid"), nullable=False)

    transactions = relationship("TransactionHistory", back_populates="portfolio")
    # User와의 관계
    user = relationship("User", back_populates="portfolios")

    # PortfolioHoldings와의 관계
    holdings = relationship("PortfolioHoldings", back_populates="portfolio")

    # PortfolioValueHistory와의 관계
    value_history = relationship("PortfolioValueHistory", back_populates="portfolio")


class PortfolioValueHistory(Base):
    __tablename__ = "portfolio_value_history"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(
        Integer, ForeignKey("portfolios.portfolio_id"), nullable=False
    )
    value = Column(DECIMAL(18, 2), nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    portfolio = relationship("Portfolio", back_populates="value_history")


class PortfolioHoldings(Base):
    __tablename__ = "portfolio_holdings"

    portfolio_id = Column(
        Integer, ForeignKey("portfolios.portfolio_id"), primary_key=True, index=True
    )
    financial_product_id = Column(
        Integer,
        ForeignKey("financial_products.financial_product_id"),
        primary_key=True,
        index=True,
    )

    currency_code = Column(String(10), nullable=False)
    price = Column(DECIMAL(18, 2), nullable=False)
    quantity = Column(DECIMAL(18, 4), nullable=False)

    # 관계 설정 변경: "FinancialProduct" -> "FinancialProducts"
    portfolio = relationship("Portfolio", back_populates="holdings")
    financial_product = relationship("FinancialProduct")
