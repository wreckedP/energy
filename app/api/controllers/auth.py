from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import  OAuth2PasswordRequestForm

from app.core.settings import env
from app.core.security import  encode_token
from app.database.crud.user import user_crud
from app.database.session import pg_session, Session


router = APIRouter()


@router.post("/token")
def get_access_token(    
    session: Annotated[Session, Depends(pg_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    OAuth2 compatible token login, set an access token for future requests
    """
    
    user = user_crud.authenticate(
        session, email=form_data.username, password=form_data.password
    )
    if user and not user.is_active:
        raise HTTPException(400, "Inactive account")
    if user:
        access_token_expires = timedelta(minutes=float(env.token_expire_minutes))
        access_token = {
            "access_token": encode_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }

        return access_token