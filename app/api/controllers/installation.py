from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from app.api.dependencies.installation import get_all_installations, installation
from app.api.dependencies.user import current_active_user, UserModel
from app.database.session import pg_session, Session, Session
from app.database.crud.installation import installation_crud, InstallationModel

from app.schemas.installation import (
    InstallationCreateDTO,
    InstallationPublic,
    InstallationUpdateDTO,
)


router = APIRouter()


@router.post("")
async def create_installation(
    create_data: InstallationCreateDTO,
    user: Annotated[UserModel, Depends(current_active_user)],
    session: Annotated[Session, Depends(pg_session)],
):

    if user.installation_id and not user.is_superuser:
        raise HTTPException(406, "You already have an installation")

    installation = installation_crud.create(session, create_data, user.email)

    user.installation_id = installation.id
    session.commit()

    return installation.to_dict()


@router.get("")
def get_installation(installation: Annotated[InstallationModel, Depends(installation)]):
    
    return installation.to_dict()


@router.put("", response_model=InstallationPublic)
def put_installation_installation(
    update_data: InstallationUpdateDTO,
    installation: Annotated[InstallationModel, Depends(installation)],
    session: Annotated[Session, Depends(pg_session)],
):
    updated_installation = installation_crud.put(
        session, installation, update_data.model_dump(exclude_none=True)
    )

    return updated_installation.to_dict()


@router.get("/all")
def all_installations(
    installation_list=Depends(get_all_installations),
):
    return installation_list
