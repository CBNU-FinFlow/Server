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

@router.get(
    "/",
    response_model=list[PortfolioOut],
    summary="포트폴리오 조회",
    responses={
        200: {"description": "포트폴리오 목록 반환"}
    }
)
def get_all_portfolios_for_user(user_id: int, db: Session = Depends(get_db)):
    """
    특정 사용자의 모든 포트폴리오를 조회.

    - **user_id**: 조회할 사용자의 ID
    - **output**: 사용자의 포트폴리오 목록
    """
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
    return portfolios

@router.post(
    "/",
    response_model=PortfolioOut,
    status_code=status.HTTP_201_CREATED,
    summary="포트폴리오 생성",
    responses={
        201: {"description": "포트폴리오 생성 성공"},
        400: {"description": "포트폴리오 이름이 이미 존재"}
    }
)
def create_portfolio(
    user_id: int, 
    portfolio_data: PortfolioCreate,
    db: Session = Depends(get_db)
):
    
    """
    새로운 포트폴리오를 생성.
    - **user_id**: 포트폴리오를 생성할 사용자의 ID
    - **portfolio_data**: 포트폴리오 정보 (portfolio_name)
    - **output**: 생성된 포트폴리오 정보
    """

 # 동일 사용자의 중복된 이름의 포트폴리오 확인
    existing_portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.user_id == user_id, Portfolio.portfolio_name == portfolio_data.portfolio_name)
        .first()
    )
    if existing_portfolio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="포트폴리오 이름이 이미 존재"
        )
    
    new_portfolio = Portfolio(
        user_id=user_id,
        portfolio_name=portfolio_data.portfolio_name
    )
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    return new_portfolio

@router.patch(
    "/{portfolio_id}",
    response_model=PortfolioOut,
    summary="포트폴리오 수정",
    responses={
        200: {"description": "포트폴리오 수정 성공"},
        400: {"description": "포트폴리오 이름이 이미 존재"},
        404: {"description": "포트폴리오를 찾을 수 없음"}
    }
)
def update_portfolio(
    portfolio_id: int,
    portfolio_data: PortfolioUpdate,
    db: Session = Depends(get_db)
):
    """
    특정 포트폴리오의 이름을 수정.

    - **portfolio_id**: 수정할 포트폴리오 ID
    - **portfolio_name**: 새로운 포트폴리오 이름
    - **output**: 수정된 포트폴리오 정보
    """

    portfolio = db.query(Portfolio).filter(Portfolio.portfolio_id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="포트폴리오를 찾을 수 없음")

 # 포트폴리오 수정 시 중복 체크
    if portfolio_data.portfolio_name is not None and portfolio_data.portfolio_name != portfolio.portfolio_name:
        duplicate_portfolio = (
            db.query(Portfolio)
            .filter(
                Portfolio.user_id == portfolio.user_id,
                Portfolio.portfolio_name == portfolio_data.portfolio_name,
                Portfolio.portfolio_id != portfolio_id
            )
            .first()
        )
        if duplicate_portfolio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="포트폴리오 이름이 이미 존재"
            )
        portfolio.portfolio_name = portfolio_data.portfolio_name

    db.commit()
    db.refresh(portfolio)
    return portfolio

@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="포트폴리오 삭제",
    responses={
        204: {"description": "포트폴리오 삭제 성공"},
        404: {"description": "포트폴리오 삭제 실패: 찾을 수 없는 경우"}
    }
)
def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """
    특정 포트폴리오를 삭제.
    - **portfolio_id**: 삭제할 포트폴리오 ID
    """
    portfolio = db.query(Portfolio).filter(Portfolio.portfolio_id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="포트폴리오 찾을 수 없음")
    db.delete(portfolio)
    db.commit()




    # 204 No Content로 응답
    return
