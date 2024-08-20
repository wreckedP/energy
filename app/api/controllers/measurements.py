from calendar import monthrange
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends

from app.api.dependencies.installation import installation, InstallationModel
from app.database.crud.measurement import measurement_crud
from app.database.session import pg_session, Session


router = APIRouter()

@router.get("/{channel_id}/day/{year}/{month}/{day}")
def day_measurements(
    channel_id: int,
    year: int,
    month: int,
    day: int,
    installation: Annotated[InstallationModel, Depends(installation)],
    session: Annotated[Session, Depends(pg_session)],
):
    date_from = datetime(year, month, day)
    
    date_till = date_from + timedelta(days=1, seconds=-1)
           
    measurements = measurement_crud.get_with_date_range(
        session,
        channel_id=channel_id,
        from_date=date_from.timestamp(),
        till_date=date_till.timestamp(),
    
    )
    return measurements


@router.get("/{channel_id}/month/{year}/{month}")
def month_measurements(
    channel_id: int,
    year: int,
    month: int,
    installation: Annotated[InstallationModel, Depends(installation)],
    session: Annotated[Session, Depends(pg_session)],
):
    date_from = datetime(year, month, 1)
    _, days_in_month = monthrange(date_from.year, date_from.month)
      
    if date_from.month == 12:
        date_till = date_from.replace(day=days_in_month) + timedelta(days=1, seconds=-1)
    else:
        date_till = date_from.replace(day=days_in_month) + timedelta(days=1)
    
    measurements = measurement_crud.get_with_date_range(
        session,    
        channel_id=channel_id,
        from_date=date_from.timestamp(),
        till_date=date_till.timestamp(),
       
    )
    return measurements
