from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError
from app.db.session import get_db
from app.models import User
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    try:
        return auth_service.register(email=str(payload.email), password=payload.password, full_name=payload.full_name)
    except AuthenticationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, auth_service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    try:
        return auth_service.login(email=str(payload.email), password=payload.password)
    except AuthenticationError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
