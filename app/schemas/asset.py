from pydantic import BaseModel
from typing import Optional


class AssetBase(BaseModel):
    asset_name: str
    asset_type: str
    quantity: float
    purchase_price: float
    current_value: Optional[float] = None
    account_id: int  # 계좌 ID 추가


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    quantity: Optional[float] = None
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None
    account_id: Optional[int] = None  # 계좌 변경 가능


class AssetTransfer(BaseModel):
    new_account_id: int  # 새 계좌 ID
    amount: float  # 이동할 금액
