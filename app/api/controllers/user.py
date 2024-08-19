from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.user import current_active_user
from app.database.models.user import UserModel
from app.database.session import pg_session
from app.database.crud.user import user_crud
from app.schemas.user import UserCreateDTO, UserUpdateSelfDTO

router = APIRouter()


@router.post("/register")
def new_user(
    create_data: UserCreateDTO,
    session: Annotated[Session, Depends(pg_session)],
):
    email_check = user_crud.get_by_email(session, email=create_data.email)
    if email_check is not None:
       raise HTTPException(400, "This email already registered to a user")

    new_user = user_crud.create(session, create_data)
    return new_user.to_dict()


@router.get("")
def get_user(current_user=Depends(current_active_user)):
    return current_user.to_dict()


@router.put("")
def put_current_user(
    update_data: UserUpdateSelfDTO,
    user: Annotated[UserModel, Depends(current_active_user)],
    session: Annotated[Session, Depends(pg_session)],
):
    updated_user = user_crud.update_self(session, user, update_data.dict(exclude_none=True))

    return updated_user.to_dict()
