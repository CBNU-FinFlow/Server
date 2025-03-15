# app/schemas/financial_product.py

from pydantic import BaseModel


class SectorInfo(BaseModel):
    """
    섹터 정보를 위한 스키마
    """
    sector_id: int
    sector_name: str

    class Config:
        orm_mode = True


class FinancialProductRead(BaseModel):
    """
    FinancialProduct 조회용 스키마
    """

    financial_product_id: int
    product_name: str
    ticker: str
    sector: SectorInfo

    class Config:
        orm_mode = True
