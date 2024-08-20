from datetime import datetime, timedelta
from typing import Any, Union
from fastapi.exceptions import HTTPException

from jose.jwt import decode, encode, JWTError
from passlib.context import CryptContext

from app.settings.configuration import configuration
from app.schemas.token import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_hash(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def encode_token(subject: Union[str, Any], expires_delta: timedelta) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=float(configuration.token_expire_minutes))
    to_encode: dict[str, Any] = {"exp": expire, "sub": str(subject)}
    encoded_jwt = encode(to_encode, configuration.private_key, algorithm="HS256")

    return encoded_jwt


def decode_token(token: str) -> TokenPayload:
    try:
        payload = decode(token, configuration.private_key, algorithms="HS256")

        return TokenPayload(**payload)

    except JWTError as error:
        raise HTTPException(403, f"Invalid token: {error}")
