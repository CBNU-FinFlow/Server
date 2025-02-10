from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate, PortfolioOut

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[PortfolioOut])
def get_all_portfolios_for_user(user_id: int, db: Session = Depends(get_db)):
    #특정 user_id의 모든 포트폴리오 조회
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
    return portfolios

@router.post("/", response_model=PortfolioOut, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    user_id: int, 
    portfolio_data: PortfolioCreate,
    db: Session = Depends(get_db)
):
    
    #포트폴리오 생성
    new_portfolio = Portfolio(
        user_id=user_id,
        total_assets=portfolio_data.total_assets,
        expected_dividend=portfolio_data.expected_dividend
    )
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    return new_portfolio

@router.patch("/{portfolio_id}", response_model=PortfolioOut)
def update_portfolio(
    portfolio_id: int,
    portfolio_data: PortfolioUpdate,
    db: Session = Depends(get_db)
):
    # 포트폴리오 수정

    portfolio = db.query(Portfolio).filter(Portfolio.portfolio_id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    # 포트폴리오 업데이트
    if portfolio_data.total_assets is not None:
        portfolio.total_assets = portfolio_data.total_assets
    if portfolio_data.expected_dividend is not None:
        portfolio.expected_dividend = portfolio_data.expected_dividend

    db.commit()
    db.refresh(portfolio)
    return portfolio

@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
  #포트폴리오 삭제
    portfolio = db.query(Portfolio).filter(Portfolio.portfolio_id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    db.delete(portfolio)
    db.commit()




    # 204 No Content로 응답
    return
