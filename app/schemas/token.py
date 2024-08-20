from pydantic import BaseModel, EmailStr

class TokenPayload(BaseModel):
    sub: int
