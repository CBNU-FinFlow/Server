# schemas/portfolio.py
from pydantic import BaseModel, condecimal
from typing import Optional

class PortfolioBase(BaseModel):
    total_assets: Optional[condecimal(max_digits=18, decimal_places=2)] = None
    expected_dividend: Optional[condecimal(max_digits=18, decimal_places=2)] = None

class PortfolioCreate(PortfolioBase):
    
    #포트폴리오 생성 시 필요한 스키마
    #여기에 추가
    
    pass

class PortfolioUpdate(PortfolioBase):
    
    #포트폴리오 수정 시 필요한 스키마
    #PATCH로 들어오는 값은 모두 optional
    pass

class PortfolioOut(BaseModel):
    
    #API 응답용 스키마
    
    portfolio_id: int
    user_id: int
    total_assets: Optional[float] = None
    expected_dividend: Optional[float] = None

    class Config:
        orm_mode = True  
