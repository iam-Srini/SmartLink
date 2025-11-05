from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import PyJWTError, InvalidTokenError, ExpiredSignatureError
from fastapi import HTTPException, status

from app.core.config import settings


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token with an expiration time and scope.
    """
    encode_data = data.copy()
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expiration_minutes
    )
    encode_data.update({"exp": expires, "scope": "access_token"})
    encoded_jwt = jwt.encode(
        payload=encode_data,
        algorithm=settings.algorithm,
        key=settings.secret_key,
    )
    print(f"Encoded data: {encoded_jwt}")
    return encoded_jwt


def verify_access_token(token: str) -> str:
    """
    Verify a JWT access token and return the user ID if valid.
    """
    try:
        payload = jwt.decode(
            token,
            key=settings.secret_key,
            algorithms=settings.algorithm,
        )
        user_id = payload.get("sub")
        scope = payload.get("scope")

        if scope != "access_token":
            raise InvalidTokenError("Invalid token: incorrect scope")

        if not user_id:
            raise InvalidTokenError("Invalid token: missing subject")

        return user_id

    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    except PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
