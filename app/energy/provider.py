from datetime import datetime
from app.core.error import HTTP_ERROR
from app.core.logger import log
from app.database.models.meter import MeterModel
from app.energy.providers import mock, energiemissie, joulz, kenter
from app.energy.providers.base_provider import BaseProvider
from app.database.schemas.channel import ChannelWithMeasurements


def energy_provider_factory(provider_name: str, api_key: str):
    match provider_name:
        case "mock":  # test / demo adapter
            return EnergyProvider(mock.MockAdapter(api_key))
        case "energiemissie":
            return EnergyProvider(energiemissie.EnergiemissieAdapter(api_key))
        case "joulz":
            return EnergyProvider(joulz.JoulzAdapter(api_key))
        # case "fudura":
        #     return (fuduraEnergyProvider.FuduraAdapter(allation.api_api_key))
        # case "tums":
        #     return (tumsEnergyProvider.TumsAdapter(allation.api_api_key))
        case "kenter":
            return EnergyProvider(kenter.KenterAdapter(api_key))
        case _:
            return HTTP_ERROR(
                404,
                f"We do not support: {provider_name} as energy provider",
            )


class EnergyProvider:
    """A service to work with different sorts of BaseProviders"""

    def __init__(self, provider: BaseProvider):
        self._provider = provider

        log.info("energyprovider used: %s", provider.__class__.__name__)

    async def fetch_meter_list(self):
        """Uses the adapter's method to get a meter list"""

        return await self._provider.fetch_meter_list()

    async def get_day_measurements(
        self, meter: MeterModel, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Uses the adapter's method to get a measuement list of a day"""

        return await self._provider.fetch_day_measurements(meter.source_id, date)

    async def get_month_measurements(
        self, meter: MeterModel, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Uses the adapter's method to get a measuement list of a month"""

        return await self._provider.fetch_month_measurements(meter.source_id, date)
