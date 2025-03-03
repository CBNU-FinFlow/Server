# schemas/transaction.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TransactionBase(BaseModel):
    portfolio_id: int
    financial_product_id: int
    transaction_type: str
    price: float
    profit_rate: Optional[float] = None
    currency_code: Optional[str] = None
    quantity: Optional[float] = None
    created_at: Optional[datetime] = None


class TransactionOut(TransactionBase):
    transaction_id: int

    class Config:
        orm_mode = True


class DeleteResponse(BaseModel):
    message: str


class TransactionCreate(TransactionBase):
    pass

# 페이징 응답을 위해 선택적으로 추가
class TransactionListResponse(BaseModel):
    total_count: int
    page: int
    per_page: int
    data: list[TransactionOut]
