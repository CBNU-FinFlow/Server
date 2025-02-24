# schemas/portfolio.py
from pydantic import BaseModel, condecimal
from typing import Optional


class PortfolioBase(BaseModel):
    portfolio_name: str


class PortfolioCreate(PortfolioBase):
    """포트폴리오 생성 시 필요한 스키마"""

    # 여기에 추가
    pass


class PortfolioUpdate(PortfolioBase):
    """포트폴리오 수정 시 필요한 스키마"""

    portfolio_name: Optional[str] = None


class PortfolioOut(BaseModel):
    """API 응답용 스키마"""

    portfolio_id: int
    user_id: int
    portfolio_name: str

    class Config:
        orm_mode = True
