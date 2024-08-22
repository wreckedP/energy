from datetime import datetime
from typing import Any

from requests import post
from app.schemas.measurements import MeasurementCreateDTO

from app.settings.logger import log
from app.database.models.meter import MeterModel
from app.energy.providers.base_provider import BaseProvider
from app.schemas.channel import ChannelWithMeasurements
from app.schemas.meter import MeterCreateDTO


class FuduraAdapter(BaseProvider):
    """A concrete implemetation working with the Kenter API"""

    def __init__(self, provider_key: str) -> None:
        self.set_access_token()
        self.base_url = "https://api.fudura.nl/telemetry"

    def set_access_token(self):
        # super().__init__({"x-api-key": provider_key})

        files = {
            "grant_type": (None, "client_credentials"),
            "resource": (
                None,
                "https://fdrwsadprd.onmicrosoft.com/FuduraWebserviceProduction",
            ),
            "client_id": (None, "client_id"),
            "client_secret": (None, "pi_key"),
        }
        post(self.base_url, files)
        return

    async def fetch_meter_list(self) -> list[MeterCreateDTO]:
        """Returns all available meters from endpoint in meter objects"""
        raw_meters = await self.make_request("/detailed-meteringpoints[?continuationToken][&customerId][&perCustomer]")
        raw_meters = {
    "meteringPoints": [{
        "ean": "123456789012345678",
        "meteringPointId": "87654321012345678",
        "authorizations": [{
            "customerId": "123",
            "periods": [{
                "from": "2019-12-31T23:00:00Z",
                "to": "2020-12-31T23:00:00Z"
            }]
        }, {
            "customerId": "456",
            "periods": [{
                "from": "2019-12-31T23:00:00Z"
            }]
        }],
        "channels": [{
            "channelId": "ELCLAx"
        }, {
            "channelId": "ELCOAx"
        }]
    }]
}
        meter_objects: list[MeterCreateDTO] = []

        for raw_meter in raw_meters["meteringPoints"]:
            meter_obj = MeterCreateDTO(
                name=raw_meter["ean"],
                commodity="",
                status="",
                ean=raw_meter["ean"],
                source_id=raw_meter["meteringPointId"],
                installed_at=raw_meter["authorizations"][0]["periods"][0]["from"]
                )
            meter_objects.append(meter_obj)
        
        return meter_objects

    async def fetch_day_measurements(self, meter: str, date: datetime):
        """Get measurement values from a meter on a speficic day"""
        return self.format_measurements()

    async def fetch_month_measurements(self, meter: str, date: datetime):
        """Get measurement values from a meter on a speficic day"""
        
        # raw_channels = self.make_request(f"/meteringpoints/{meter}/channels[?customerId]")
        raw_channels = {
    "channels": ["ELCLAx15", "ELCOAx15", "ELCSAx15"]
}

        measurements_per_channel: list[ChannelWithMeasurements] = []
    

        for raw_channel in raw_channels["channels"]:
            # raw_measurements = self.make_request(f"/meteringpoints/{meter}/channels/{channelId}/query[?from][&to][&continuationToken][&customerId]")
            raw_measurements = {
            "telemetry": [{
                "value": "13.37",
                "readingTimestamp": "2021-01-01T00:00:00Z",
                "tariff": "Normal",
                "isValid": True,
                "repairStatus": "Estimated"
            }, {
                "value": "18",
                "readingTimestamp": "2021-01-01T01:00:00Z"
            }],
            "continuationToken": "c29tZSBhcmJpdHJhcnkgY29udGludWF0aW9uIHRva2Vu"
        }
            measurements: list[MeasurementCreateDTO] = []

            for raw_measurement in raw_measurements["telemetry"]:
                measurements.append(MeasurementCreateDTO(
                    value=raw_measurement["value"],
                    timestamp=raw_measurement["readingTimestamp"]
                ))
                
            measurements_per_channel.append(
                ChannelWithMeasurements(
                    channel_name=raw_channel, 
                    measurements=measurements
                    )
                )
        return measurements_per_channel

    def format_measurements(
        self, raw_measurements: list[dict[str, Any]]
    ) -> list[ChannelWithMeasurements]:
        return


if __name__ == "__main__":
    provider = FuduraAdapter("")
    meters = provider.fetch_meter_list()
    print(meters)
