from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUser, get_current_user
from app.database.session import get_db
from app.modules.auth.schemas import (
    AuthMeResponse,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
)
from app.modules.auth.service import AuthService
from app.shared.responses import MessageResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return AuthService.register(db, payload)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return AuthService.login(db, payload)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshTokenRequest) -> TokenResponse:
    return TokenResponse(access_token=payload.refresh_token, refresh_token=payload.refresh_token)


@router.post("/logout", response_model=MessageResponse)
def logout(current_user: CurrentUser = Depends(get_current_user)) -> MessageResponse:
    return MessageResponse(message=f"Logged out user {current_user.user_id}")


@router.get("/me", response_model=AuthMeResponse)
def get_me(current_user: CurrentUser = Depends(get_current_user)) -> AuthMeResponse:
    return AuthMeResponse(user_id=current_user.user_id, roles=current_user.roles)
