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

def encrypt(data: dict[str, Any]):
    return encode(data, configuration.private_key, algorithm="HS256")

def decrypt(token: str):
    return decode(token, configuration.private_key, algorithms="HS256")

def encode_token(subject: Union[str, Any], expires_delta: timedelta) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=float(configuration.token_expire_minutes))

    return encrypt({
        "exp": expire, 
        "sub": str(subject)
        })


def decode_token(token: str) -> TokenPayload:
    try:
        return TokenPayload(**decrypt(token))

    except JWTError as error:
        raise HTTPException(403, f"Invalid token: {error}")
