from abc import ABC, abstractmethod
from datetime import datetime

from fastapi.exceptions import HTTPException
import msgspec
from httpx import AsyncClient


from app.schemas.channel import ChannelWithMeasurements
from app.schemas.meter import MeterCreateDTO


class BaseProvider(ABC):
    """ABC for different measurement providers"""

    def __init__(self, headers: dict[str, str] | None):
        """Initialize the provider instance"""
        self.headers = headers

    async def make_request(self, url: str):
        """Make get request with instance's session"""

        async with AsyncClient(headers=self.headers, timeout=120) as client:
            response = await client.get(url)

        match response.status_code:
            case 200:
                response = msgspec.json.decode(response.content)
                return response

            case 401:
                print("adapter response:\n{response}")
                raise HTTPException(404, "Credentials failed to authenticate on provider")

            case _:
                return [{"unhandled exception": response}]

    @abstractmethod
    async def fetch_meter_list(self) -> list[MeterCreateDTO]:
        pass

    @abstractmethod
    async def fetch_day_measurements(
        self, source_id: str, date: datetime
    ) -> list[ChannelWithMeasurements]:
        pass

    @abstractmethod
    async def fetch_month_measurements(
        self, source_id: str, date: datetime
    ) -> list[ChannelWithMeasurements]:
        pass
