import time
from collections import defaultdict
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError
from app.db.session import get_db
from app.models import User

settings = get_settings()
request_log = defaultdict(list)


class RateLimiter:
    def __init__(self, limit: int = 60, window_seconds: int = 60) -> None:
        self.limit = limit
        self.window_seconds = window_seconds

    def __call__(self, request: Request) -> None:
        client_id = request.client.host if request.client else "unknown"
        now = int(time.time())
        timestamps = request_log[client_id]
        timestamps[:] = [ts for ts in timestamps if now - ts < self.window_seconds]
        if len(timestamps) >= self.limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        timestamps.append(now)


rate_limiter = RateLimiter(limit=settings.rate_limit_per_minute)


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    authorization = request.headers.get("authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
