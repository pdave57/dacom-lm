from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token
from app.modules.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from app.shared.enums import RoleEnum


class AuthService:
    """Authentication business logic."""

    @staticmethod
    def register(db: Session, payload: RegisterRequest) -> TokenResponse:
        # TODO: Persist user with hashed password and assign PARTICIPANT role.
        access_token = create_access_token(
            subject=payload.email, roles=[RoleEnum.PARTICIPANT.value]
        )
        refresh_token = create_refresh_token(subject=payload.email)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def login(db: Session, payload: LoginRequest) -> TokenResponse:
        # TODO: Verify credentials against users table and issue tokens.
        access_token = create_access_token(
            subject=payload.email, roles=[RoleEnum.PARTICIPANT.value]
        )
        refresh_token = create_refresh_token(subject=payload.email)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
