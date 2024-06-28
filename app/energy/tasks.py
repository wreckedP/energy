from app.database.models.meter import MeterModel
from app.energy.helpers import (
    calculate_dates,
    update_month_measurements,
    update_single_meter_known_channels,
)
from app.energy.provider import EnergyProvider
from app.database.crud.meter import meter_crud
from app.core.logger import log
from datetime import datetime, timedelta

from app.database.session import session

# session = pg_session()


async def update_meter_from_remote(installation_id: int, provider: EnergyProvider):
    new_meters: list[MeterModel] = []
    local_meters: list[MeterModel] = []

    remote_meters = await provider.fetch_meter_list()

    for meter in remote_meters:
        local_meter = meter_crud.get_by_source_id(session, meter.source_id)
        if local_meter is None:
            new_meter = meter_crud.create(session, meter, installation_id)
            new_meters.append(new_meter)
        else:
            local_meters.append(local_meter)

    log.info(
        "installation_id: %s | %s remote meter(s) | %s local meter(s) | %s new meter(s)",
        installation_id,
        len(remote_meters),
        len(local_meters),
        len(new_meters),
    )
    return local_meters + new_meters


async def update_measurements_from_remote(
    installation_id: int, provider: EnergyProvider
):
    last_known = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
        days=365 * 5
    )
    meters = await update_meter_from_remote(installation_id, provider)

    for meter in meters:
        last_known = update_single_meter_known_channels(meter, last_known)

        num_months = calculate_dates(last_known)

        log.info(
            "updating meter: %s id: %s since: %s", meter.name, meter.id, last_known
        )

        await update_month_measurements(
            meter, last_known, num_months, provider, session
        )

    return f"updated measurements of {len(meters)} meters"


async def calculate_month_accumulatation():
    # TODO:
    pass
