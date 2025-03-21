# app/schemas/asset.py

from pydantic import BaseModel
from typing import Optional, List
from app.schemas.financial_product import FinancialProductRead
from datetime import datetime


class AssetBase(BaseModel):
    portfolio_id: int
    financial_product_id: int
    currency_code: str
    price: float
    quantity: float


class AssetCreate(BaseModel):
    """보유 자산 생성 시 필요한 스키마"""

    portfolio_id: int
    financial_product_id: int
    currency_code: str
    price: float
    quantity: float
    transaction_type: str  # 거래 종류 (구매/판매)
    transaction_date: datetime  # 거래 날짜

    class Config:
        orm_mode = True


class AssetUpdate(BaseModel):
    portfolio_id: int
    financial_product_id: int
    currency_code: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[float] = None


class AssetRead(BaseModel):
    """보유 자산 조회 응답 모델 (financial_product 포함)"""

    portfolio_id: int
    currency_code: str
    price: float
    quantity: float
    financial_product: FinancialProductRead

    class Config:
        orm_mode = True


class AssetPageResponse(BaseModel):
    """페이징을 포함한 보유 자산 목록 응답 모델"""

    total: int
    page: int
    per_page: int
    assets: List[AssetRead]
