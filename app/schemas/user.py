# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    investment_profile: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    investment_profile: Optional[str] = None

class UserOut(BaseModel):
    uid: int
    name: str
    email: str
    investment_profile: Optional[str] = None

    class Config:
        orm_mode = True