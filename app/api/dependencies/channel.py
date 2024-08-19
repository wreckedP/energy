from typing import Annotated
from fastapi import Depends
from fastapi.exceptions import HTTPException
from app.api.dependencies.installation import installation

from app.database.crud.channel import channel_crud
from app.database.models.channel import ChannelModel
from app.database.models.installation import InstallationModel
from app.database.session import pg_session, Session


# def create_channel(
#     create_data: ChannelCreateDTO,
#     meter=Depends(meter_of_installation_by_id),
#     session=Depends(pg_session),
# ):
#     new_channel = channel_crud.create(session, create_data, meter.id)

#     return new_channel


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

    raise HTTPException(400, "You do not have enough privileges")