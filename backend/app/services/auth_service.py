from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError
from app.models import User

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
settings = get_settings()


class AuthService:
    def __init__(self, session: Session):
        self.session = session

    def register(self, *, email: str, password: str, full_name: Optional[str] = None) -> dict[str, str]:
        if self.session.query(User).filter(User.email == email).first():
            raise AuthenticationError("User already exists")

        user = User(email=email, hashed_password=self._hash_password(password), full_name=full_name)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return self._create_token_response(user)

    def login(self, *, email: str, password: str) -> dict[str, str]:
        user = self.session.query(User).filter(User.email == email).first()
        if not user or not self._verify_password(password, user.hashed_password or ""):
            raise AuthenticationError("Invalid credentials")
        return self._create_token_response(user)

    def _create_token_response(self, user: User) -> dict[str, str]:
        access_token = self._create_access_token(user)
        refresh_token = self._create_refresh_token(user)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def _create_access_token(self, user: User) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
        payload = {"sub": str(user.id), "exp": expires_at, "type": "access"}
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    def _create_refresh_token(self, user: User) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_token_expire_days)
        payload = {"sub": str(user.id), "exp": expires_at, "type": "refresh"}
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)
