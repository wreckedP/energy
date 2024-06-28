from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.channel import channel_of_meter_by_id
from app.database.models.channel import ChannelModel
from app.database.crud.channel import channel_crud
from app.database.session import pg_session
from app.database.schemas.channel import ChannelUpdateDTO

router = APIRouter()


@router.put("/{channel_id}/qanteon_name")
async def put_channel_qanteon_name(
    updated_data: ChannelUpdateDTO,
    channel: Annotated[ChannelModel, Depends(channel_of_meter_by_id)],
    session: Annotated[Session, Depends(pg_session)],
):
    updated_channel = channel_crud.put(
        session, channel, updated_data.dict(exclude_none=True)
    )
    return updated_channel.to_dict()
