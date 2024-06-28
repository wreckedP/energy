from calendar import monthrange
from datetime import datetime, timedelta

from app.core.logger import log
from app.database.crud.channel import channel_crud
from app.database.crud.measurement import measurement_crud
from app.database.models.channel import ChannelModel
from app.database.models.meter import MeterModel
from app.database.schemas.measurements import MeasurementCreateDTO
from app.energy.provider import EnergyProvider


def calculate_dates(last_known):
    today = datetime.today().replace(hour=0, minute=0, second=0)
    num_months = (
        (today.year - last_known.year) * 12 + (today.month - last_known.month) + 1
    )
    return num_months


def update_single_meter_known_channels(meter, last_known):
    if meter.channels is not None:
        for channel in meter.channels:
            if channel.latest_measurement is None:
                log.critical("NO latest_measurement on channel whilst channel is known")
            else:
                last_known = datetime.fromtimestamp(channel.latest_measurement)
    return last_known


def handle_measurement_writing(measurements_list: list[MeasurementCreateDTO], local_channel: ChannelModel, session):
    log.info(
        "writting %s measurements to channel_id: %s",
        len(measurements_list),
        local_channel.id,
    )
    if len(measurements_list) > 0:
        for measurement in measurements_list:
            measurement_crud.create(session, measurement, local_channel.id)
        channel_crud.put(
            session,
            local_channel,
            {"latest_measurement": measurements_list[-1].timestamp},
        )
        session.commit()


async def update_month_measurements(
    meter: MeterModel,
    last_known: datetime,
    num_months: int,
    provider: EnergyProvider,
    session,
):
    for _ in range(num_months):
        for measurements_list in await provider.get_month_measurements(
            meter, last_known
        ):
            if measurements_list.channel_name not in meter.channels:
                local_channel = channel_crud.get_by_channel_name_and_meter(
                    session, measurements_list.channel_name, meter.id
                )
            else:
                local_channel = next(
                    (
                        channel
                        for channel in meter.channels
                        if channel.name == measurements_list.channel_name
                    )
                )
            filtered_measurements = filter(
                lambda m: datetime.fromtimestamp(m.timestamp) > last_known,
                measurements_list.measurements
            )
            handle_measurement_writing(list(filtered_measurements), local_channel, session)

        _, days_in_month = monthrange(last_known.year, last_known.month)
        last_known = last_known.replace(day=days_in_month) + timedelta(days=1)
