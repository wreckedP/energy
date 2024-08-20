from typing import Annotated
from fastapi import Depends

from app.api.dependencies.installation import installation, InstallationModel


async def meter_of_installation_by_id(
    meter_id: int,
    installation: Annotated[ InstallationModel, Depends(installation)],
):
    for meter in installation.meters:
        if meter.id == meter_id:
            return meter
