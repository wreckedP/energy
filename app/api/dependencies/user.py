from typing import Annotated
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.settings.security import decode_token
from app.database.crud.user import user_crud, UserModel
from app.database.session import pg_session, Session

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def get_current_user(
    session: Annotated[Session, Depends(pg_session)],
    token: Annotated[str, Depends(oauth2)],
) -> UserModel | None:
    """
    Use JWT token to get user id
    """

    token_data = decode_token(token)
    if token_data:
        return user_crud.get(session, token_data.sub)


def current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> UserModel:

    if not current_user.is_active:
        raise HTTPException(401, "Inactive account")

    return current_user


def current_active_superuser(
    current_user: Annotated[UserModel, Depends(current_active_user)],
) -> UserModel:

    if not current_user.is_superuser:
        raise HTTPException(401, "You do not have enough privileges")

    return current_user
