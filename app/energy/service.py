from calendar import monthrange
from datetime import datetime, timedelta

from app.schemas.channel import ChannelWithMeasurements
from app.database.session import session
from app.database.crud.meter import meter_crud, MeterModel
from app.database.crud.channel import channel_crud
from app.database.crud.measurement import measurement_crud
from app.database.crud.installation import installation_crud
from app.energy.provider import get_platform

async def update_meters(installation_id: int, name: str, key: str):
    """Uses the adapter's method to get a meter list"""

    new_meters: list[MeterModel] = []
    local_meters: list[MeterModel] = []

    platform = get_platform(name, key)
    remote_meters = await platform.fetch_meter_list()

    for meter in remote_meters:
        local_meter = meter_crud.get_by_source_id(session, meter.source_id)
        if local_meter is None:
            new_meter = meter_crud.create(
                session, meter, installation_id
            )
            new_meters.append(new_meter)
        else:
            local_meters.append(local_meter)

    return f"fetched meters: {len(local_meters + new_meters)}"


async def update_measurements(installation_id: int, name: str, key: str):

    today = datetime.today()
    five_years_ago = today - timedelta(days=365 * 5)
    last_known = five_years_ago.replace(month=1, day=1, hour=0, minute=0, second=0)
    
    platform = get_platform(name, key)
    installation = installation_crud.get_with_meters(session, installation_id)

    for meter in installation.meters:

        meter_with_channels = meter_crud.get_by_id_with_channels(session, meter.id)

        if meter_with_channels and meter_with_channels.channels is not None:
            for channel in meter.channels:
                latest_check = datetime.fromtimestamp(channel.latest_measurement)
                # TODO fix, now checking only for most recent, missing, known measurement of channels
                if latest_check is not None and latest_check > last_known:
                    print(f"FOUND LAST_KOWN: {last_known}")
                    last_known = latest_check

        num_months = (
            (today.year - last_known.year) * 12 + (today.month - last_known.month) + 1
        )
        for _ in range(num_months):
            measurements = await platform.fetch_month_measurements(meter.source_id, last_known)
            
            for measuement in measurements:
                write_measurements(meter.id, measuement)

            _, days_in_month = monthrange(last_known.year, last_known.month)
            last_known = last_known.replace(day=days_in_month) + timedelta(days=1)
            
        session.commit()
        

    return f"up-to-date meters: {len(installation.meters)}"



def write_measurements(
    meter_id: int,
    channel_data: ChannelWithMeasurements,
):
    """
    write measurements for each given channel for the meter
    """

    local_channel = channel_crud.get_by_channel_name_and_meter(
        session, channel_data.channel_name, meter_id
    )
    print(
        "writting %s measurements to channel_id: %s",
        len(channel_data.measurements),
        local_channel.id,
    )
    for meausurement in channel_data.measurements:
        try:
            measurement_crud.create(session, meausurement, local_channel.id)
        except (SQLAlchemyError, DBAPIError, StatementError, DataError):
            session.rollback()

    channel_crud.put(
        session,
        local_channel,
        {"latest_measurement": channel_data.measurements[-1].timestamp},
    )
