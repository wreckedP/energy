from datetime import datetime

from fastapi import BackgroundTasks, Depends

from app.api.dependencies.installation import (
    with_owner,
    provider_of_installation,
)
from app.database.crud.measurement import measurement_crud
from app.database.session import pg_session
from app.database.crud.meter import meter_crud

# def create_measurement(
#     channel_id: int,
#     create_data: MeasurementCreateDTO,
#     installation=Depends(with_owner),
#     session=Depends(pg_session),
# ):
#     measurement = measurement_crud.create(session, create_data, channel_id)

#     return measurement


def delete_measurements_range(
    channel_id: int,
    epoch_since: float,
    installation=Depends(with_owner),
    session=Depends(pg_session),
):
    measurement_crud.delete_since(session, channel_id, epoch_since)

    return "success"


async def update_day_measurement_from_provider(
    meter_id: int,
    day: int,
    month: int,
    year: int,
    do: BackgroundTasks,
    session=Depends(pg_session),
    provider=Depends(provider_of_installation),
):
    meter = meter_crud.get(session, id=meter_id)

    do.add_task(
        provider.fetch_day_measurements,
        session,
        meter,
        datetime(year, month, day).timestamp(),
    )

    return "Task is running in background"


async def update_month_measurement_from_provider(
    meter_id: int,
    month: int,
    year: int,
    do: BackgroundTasks,
    session=Depends(pg_session),
    provider=Depends(provider_of_installation),
):
    do.add_task(
        provider.fetch_month_measurements,
        session,
        meter_id,
        datetime(year, month, day=1).timestamp(),
    )

    return "Task is running in background"
