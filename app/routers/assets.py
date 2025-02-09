# app/routers/assets.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.asset import Asset
from app.models.user import User
from app.schemas.asset import AssetCreate, AssetUpdate, AssetOut
from app.routers.users import get_current_user

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("/", response_model=List[AssetOut])
def get_assets(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """현재 유저의 보유 자산 목록을 조회"""
    return db.query(Asset).filter(Asset.user_id == current_user.uid).all()


@router.post("/", response_model=AssetOut)
def create_asset(
    asset_data: AssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """새로운 자산 추가"""
    new_asset = Asset(**asset_data.dict(), user_id=current_user.uid)
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset


@router.patch("/{asset_id}", response_model=AssetOut)
def update_asset(
    asset_id: int,
    asset_data: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """자산 정보 수정"""
    asset = (
        db.query(Asset)
        .filter(Asset.asset_id == asset_id, Asset.user_id == current_user.uid)
        .first()
    )
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    for key, value in asset_data.dict(exclude_unset=True).items():
        setattr(asset, key, value)

    db.commit()
    db.refresh(asset)
    return asset


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """자산 삭제"""
    asset = (
        db.query(Asset)
        .filter(Asset.asset_id == asset_id, Asset.user_id == current_user.uid)
        .first()
    )
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    db.delete(asset)
    db.commit()
    return {"detail": "Asset deleted successfully"}
