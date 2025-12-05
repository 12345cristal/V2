# app/core/security.py
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==========================
# HASH / VERIFICACIÓN
# ==========================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# ==========================
# JWT TOKENS
# ==========================

def _create_token(
    subject: Any,
    expires_delta: timedelta,
    secret_key: str,
    token_type: str,
    extra_claims: Optional[Dict[str, Any]] = None,
) -> str:
    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "type": token_type,
        "exp": datetime.utcnow() + expires_delta,
        "iat": datetime.utcnow(),
    }
    if extra_claims:
        to_encode.update(extra_claims)

    encoded_jwt = jwt.encode(
        to_encode,
        secret_key,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def create_access_token(
    subject: Any,
    extra_claims: Optional[Dict[str, Any]] = None,
) -> str:
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(
        subject=subject,
        expires_delta=expires,
        secret_key=settings.JWT_SECRET_KEY,
        token_type="access",
        extra_claims=extra_claims,
    )


def create_refresh_token(
    subject: Any,
    extra_claims: Optional[Dict[str, Any]] = None,
) -> str:
    expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    return _create_token(
        subject=subject,
        expires_delta=expires,
        secret_key=settings.JWT_REFRESH_SECRET_KEY,
        token_type="refresh",
        extra_claims=extra_claims,
    )


def decode_token(token: str, token_type: str = "access") -> Dict[str, Any]:
    """
    Decodifica el token y valida que el tipo sea el esperado (access / refresh).
    """
    try:
        if token_type == "access":
            secret = settings.JWT_SECRET_KEY
        else:
            secret = settings.JWT_REFRESH_SECRET_KEY

        payload = jwt.decode(
            token,
            secret,
            algorithms=[settings.JWT_ALGORITHM],
        )
        if payload.get("type") != token_type:
            raise JWTError("Invalid token type")

        return payload
    except JWTError as e:
        raise e
