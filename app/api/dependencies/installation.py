from typing import Annotated
from fastapi import Depends
from fastapi.exceptions import HTTPException

from app.api.dependencies.user import current_active_superuser, current_active_user
from app.database.session import pg_session, Session
from app.database.models.user import UserModel
from app.database.crud.installation import installation_crud, InstallationModel
from app.energy.provider import EnergyProvider


# Guard dependencies

def installation(
    session: Annotated[Session, Depends(pg_session)],
    current_user: Annotated[UserModel, Depends(current_active_user)],
    installation_id: int | None = None,
) -> InstallationModel | None:

    if installation_id and not current_user.is_superuser: 
        raise HTTPException(400, "You do not have enough privileges")

    if installation_id and current_user.is_superuser: 
        installation = installation_crud.get(session, installation_id)
        return installation

    if current_user.installation_id:
        installation = installation_crud.get(
            session, current_user.installation_id
        )
        return installation


def provider_of_installation(
    installation: Annotated[InstallationModel, Depends(installation)],
) -> EnergyProvider | None:

    if installation.id and installation.provider_name and installation.provider_key :
        return EnergyProvider(installation.id, installation.provider_name, installation.provider_key)


# SU dependencies


def get_all_installations(
    session: Annotated[Session, Depends(pg_session)],
    current_user: Annotated[UserModel, Depends(current_active_superuser)],
    skip: int | None = None,
    limit: int | None = None,
) -> list[InstallationModel]:

    installations = installation_crud.get_multi(session, skip=skip, limit=limit)

    return installations