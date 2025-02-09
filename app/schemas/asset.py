# app/schemas/asset.py
from pydantic import BaseModel
from typing import Optional


class AssetBase(BaseModel):
    asset_name: str
    asset_type: str
    quantity: float
    purchase_price: float
    current_value: Optional[float] = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    quantity: Optional[float] = None
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None


class AssetOut(AssetBase):
    asset_id: int
    user_id: int

    class Config:
        orm_mode = True
