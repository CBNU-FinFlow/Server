# app/schemas/financial_product.py

from pydantic import BaseModel


class FinancialProductRead(BaseModel):
    """
    FinancialProduct 조회용 스키마
    """

    financial_product_id: int
    product_name: str
    ticker: str

    class Config:
        orm_mode = True
