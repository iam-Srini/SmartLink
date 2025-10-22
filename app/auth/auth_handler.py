import jwt
from jwt.exceptions import PyJWTError, InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from fastapi import HTTPException, status

def create_access_token(data: dict) -> str:
    encode_data = data.copy()
    expires = datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expiration_minutes)
    encode_data.update({"exp":expires, "scope":"access_token"})
    encoded_jwt = jwt.encode(payload=encode_data,algorithm=settings.algorithm,key=settings.secret_key)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token,key=settings.secret_key,algorithms=settings.algorithm)
        user_email = payload.get("sub")
        scope = payload.get("scope")

        if scope != "access_token":
            raise InvalidTokenError("Invalid Token: Incorrect Scope")
        
        if not user_email:
            raise InvalidTokenError("Invalid Token: Missing Subject")
        
        return user_email
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    except PyJWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Access token",
            headers={"WWW-Authenticate":"Bearer"},
        )
    
    