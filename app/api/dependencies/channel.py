from typing import Annotated
from fastapi import Depends
from app.api.dependencies.installation import installation

from app.database.crud.channel import channel_crud
from app.database.models.installation import InstallationModel
from app.database.session import pg_session, Session


async def channel_of_meter_by_id(
    channel_id: int,
    session: Annotated[ Session, Depends(pg_session)],
    installation: Annotated[ InstallationModel, Depends(installation)],
):
    channel = channel_crud.get(session, id=channel_id)
    if channel:
        for meter in installation.meters:
            if channel.meter_id == meter.id:
                return channel