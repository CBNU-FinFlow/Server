# app/routers/assets.py

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List

from app.db.database import SessionLocal
from app.models.portfolio import PortfolioHoldings
from app.schemas.asset import (
    AssetRead,
    AssetCreate,
    AssetUpdate,
    AssetBase,
    AssetPageResponse,
)
from app.schemas.financial_product import FinancialProductRead

router = APIRouter(prefix="/assets", tags=["Assets"])


def get_db():
    """
    요청마다 DB 세션 생성/해제
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/",
    response_model=AssetPageResponse,
    summary="보유 자산 조회 (페이징 지원 + FinancialProduct 포함)",
    responses={
        200: {"description": "자산 목록을 성공적으로 조회함."},
        400: {"description": "잘못된 요청 파라미터."},
    },
)
def read_assets(
    page: int = Query(1, ge=1, description="페이지 번호 (1부터 시작)"),
    per_page: int = Query(
        10, ge=1, le=100, description="페이지당 표시할 개수 (최대 100)"
    ),
    db: Session = Depends(get_db),
):
    """
    **보유 자산 목록을 조회하는 API (페이징 지원).**

    - `financial_product_id` 대신 `financial_product` 객체를 포함하여 반환합니다.
    - `portfolio_id`, `currency_code`, `price`, `quantity` 등의 정보를 제공합니다.

    **Response:**
    - `200 OK`: 성공적으로 자산 목록을 반환
    - `400 Bad Request`: 요청이 잘못되었을 경우
    """
    offset = (page - 1) * per_page
    total = db.query(PortfolioHoldings).count()  # 전체 데이터 개수

    holdings_query = db.query(PortfolioHoldings).offset(offset).limit(per_page).all()

    # financial_product 정보를 포함하여 응답 리스트 구성
    results = [
        AssetRead(
            portfolio_id=holding.portfolio_id,
            currency_code=holding.currency_code,
            price=holding.price,
            quantity=holding.quantity,
            financial_product=FinancialProductRead(
                financial_product_id=holding.financial_product.financial_product_id,
                product_name=holding.financial_product.product_name,
                ticker=holding.financial_product.ticker,
            ),
        )
        for holding in holdings_query
    ]

    return AssetPageResponse(total=total, page=page, per_page=per_page, assets=results)


@router.post(
    "/",
    response_model=AssetRead,
    summary="보유 자산 추가",
    responses={
        201: {"description": "자산이 성공적으로 추가됨."},
        400: {"description": "이미 존재하는 자산."},
    },
)
def create_asset(asset_data: AssetCreate, db: Session = Depends(get_db)):
    """
    **새로운 보유 자산을 추가하는 API.**

    - 요청 본문에 `portfolio_id`, `financial_product_id`, `currency_code`, `price`, `quantity`를 포함해야 합니다.

    **Response:**
    - `201 Created`: 성공적으로 자산이 추가됨
    - `400 Bad Request`: 이미 존재하는 자산일 경우
    """
    existing = (
        db.query(PortfolioHoldings)
        .filter_by(
            portfolio_id=asset_data.portfolio_id,
            financial_product_id=asset_data.financial_product_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="이미 해당 보유 자산이 존재합니다.")

    new_asset = PortfolioHoldings(
        portfolio_id=asset_data.portfolio_id,
        financial_product_id=asset_data.financial_product_id,
        currency_code=asset_data.currency_code,
        price=asset_data.price,
        quantity=asset_data.quantity,
    )
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset


@router.patch(
    "/",
    response_model=List[AssetRead],
    summary="보유 자산 수정",
    responses={
        200: {"description": "자산이 성공적으로 수정됨."},
        400: {"description": "잘못된 요청 데이터."},
    },
)
def update_assets(updates: List[AssetUpdate], db: Session = Depends(get_db)):
    """
    **보유 자산 정보를 수정하는 API.**

    - `portfolio_id`, `financial_product_id`를 기준으로 자산을 찾고, 해당 항목을 업데이트함.

    **Response:**
    - `200 OK`: 성공적으로 자산이 수정됨
    - `400 Bad Request`: 요청이 잘못되었을 경우
    """
    updated_assets = []
    for upd in updates:
        asset = (
            db.query(PortfolioHoldings)
            .filter_by(
                portfolio_id=upd.portfolio_id,
                financial_product_id=upd.financial_product_id,
            )
            .first()
        )

        if not asset:
            # 존재하지 않는 자산인 경우, 무시하거나 예외를 던질 수 있음
            continue

        if upd.currency_code is not None:
            asset.currency_code = upd.currency_code
        if upd.price is not None:
            asset.price = upd.price
        if upd.quantity is not None:
            asset.quantity = upd.quantity

        db.add(asset)
        updated_assets.append(asset)

    db.commit()

    for asset in updated_assets:
        db.refresh(asset)

    return updated_assets


@router.delete(
    "/",
    summary="보유 자산 삭제",
    responses={
        200: {"description": "자산이 성공적으로 삭제됨."},
        400: {"description": "잘못된 요청 데이터."},
    },
)
def delete_assets(
    assets_to_delete: List[AssetBase] = Body(...), db: Session = Depends(get_db)
):
    """
    **보유 자산을 삭제하는 API.**

    - `portfolio_id`, `financial_product_id`를 기준으로 해당 자산을 삭제합니다.

    **Response:**
    - `200 OK`: 성공적으로 삭제됨
    - `400 Bad Request`: 요청이 잘못되었을 경우
    """
    for asset_data in assets_to_delete:
        target = (
            db.query(PortfolioHoldings)
            .filter_by(
                portfolio_id=asset_data.portfolio_id,
                financial_product_id=asset_data.financial_product_id,
            )
            .first()
        )
        if target:
            db.delete(target)

    db.commit()
    return {"detail": "선택된 보유 자산이 삭제되었습니다."}
