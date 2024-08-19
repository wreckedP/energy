from typing import Annotated
from fastapi import Depends
from fastapi.exceptions import HTTPException

from app.api.dependencies.installation import (
    installation,
)
from app.database.models.installation import InstallationModel

# Guard dependencies

async def meter_of_installation_by_id(
    meter_id: int,
    installation: Annotated[ InstallationModel, Depends(installation)],
):
    for meter in installation.meters:
        if meter.id == meter_id:
            return meter
        
    raise HTTPException(400, "You do not have enough privileges")
