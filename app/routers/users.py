# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.responses import JSONResponse

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.core.security import create_access_token, decode_access_token

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(
    token: str = Depends(lambda token: token), db: Session = Depends(get_db)
) -> User:
    """
    JWT 토큰으로부터 현재 유저 정보를 가져옵니다.

    - **토큰이 없거나 유효하지 않은 경우**: 403 Forbidden 상태 코드를 반환합니다.
    - **토큰 디코딩 실패, payload 이상, 혹은 유저 미존재** 시에도 403을 반환합니다.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token is missing"
        )

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )

    user_id: int = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token payload"
        )

    user = db.query(User).filter(User.uid == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not found"
        )

    return user


@router.post(
    "/signup",
    response_model=UserOut,
    summary="회원가입",
    description="새로운 유저를 등록합니다. 이메일 중복 여부를 확인하며, 비밀번호는 암호화되어 저장됩니다.",
    response_description="등록된 유저 정보를 반환합니다.",
    responses={400: {"description": "Email already registered"}},
)
def signup(user_create: UserCreate, db: Session = Depends(get_db)):
    """유저 회원가입 API"""
    # 이메일 중복 체크
    exist_user = db.query(User).filter(User.email == user_create.email).first()
    if exist_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_create.password)
    new_user = User(
        name=user_create.name,
        email=user_create.email,
        password=hashed_password,
        investment_profile=user_create.investment_profile,
        profile_image=user_create.profile_image,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get(
    "/login",
    summary="로그인",
    description=(
        "유저의 이메일과 비밀번호를 확인한 후 JWT 토큰을 발급합니다. \n"
        "파라미터는 쿼리 스트링을 통해 전달됩니다."
    ),
    response_description="JWT 토큰과 유저 정보를 반환합니다.",
    responses={401: {"description": "Invalid email or password"}},
)
def login(email: str, password: str, db: Session = Depends(get_db)):
    """
    유저 로그인 API (GET 요청)

    **쿼리 파라미터**
    - **email**: 유저 이메일
    - **password**: 유저 비밀번호
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # JWT 토큰 생성
    access_token = create_access_token(data={"sub": str(user.uid)})

    # User 객체를 UserOut 모델로 변환하여 반환
    user_out = UserOut.from_orm(user)  # UserOut 모델로 변환
    return JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_out.dict(),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )


@router.patch(
    "/{user_id}",
    response_model=UserOut,
    summary="유저 정보 수정",
    description=(
        "토큰으로 인증된 유저가 본인의 정보를 수정합니다. \n"
        "수정 가능한 필드는 이름, 비밀번호, 투자 프로필, 프로필 이미지입니다."
    ),
    response_description="수정된 유저 정보를 반환합니다.",
    responses={
        403: {"description": "Not authorized to update this user or invalid token"},
        404: {"description": "User not found"},
    },
)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """유저 정보 수정 API"""
    # 본인의 정보만 수정 가능하도록 간단 로직 예시 (권한체크)
    if current_user.uid != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    user = db.query(User).filter(User.uid == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.name is not None:
        user.name = user_update.name
    if user_update.password is not None:
        user.password = get_password_hash(user_update.password)
    if user_update.investment_profile is not None:
        user.investment_profile = user_update.investment_profile
    if user_update.profile_image is not None:
        user.profile_image = user_update.profile_image

    db.commit()
    db.refresh(user)
    return user


@router.delete(
    "/{user_id}",
    summary="유저 삭제",
    description="토큰으로 인증된 유저가 본인의 계정을 삭제합니다.",
    response_description="삭제 결과 메시지를 반환합니다.",
    responses={
        403: {"description": "Not authorized to delete this user or invalid token"},
        404: {"description": "User not found"},
    },
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """유저 삭제 API"""
    if current_user.uid != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )

    user = db.query(User).filter(User.uid == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}


@router.post(
    "/logout",
    summary="로그아웃",
    description=(
        "유저 로그아웃 API. 서버는 클라이언트의 쿠키에 저장된 토큰을 삭제합니다. \n"
        "클라이언트는 쿠키 또는 로컬스토리지에서 토큰을 제거해야 합니다."
    ),
    response_description="로그아웃 결과 메시지를 반환합니다.",
    responses={403: {"description": "Token is missing or invalid"}},
)
def logout(response: Response, current_user: User = Depends(get_current_user)):
    """
    유저 로그아웃 API

    서버는 클라이언트의 쿠키 또는 로컬스토리지에 저장된 토큰을 제거하도록 안내합니다.
    """
    # 쿠키를 사용하는 경우 서버에서 쿠키 삭제
    response.delete_cookie(key="access_token")

    return {"detail": "Successfully logged out"}
