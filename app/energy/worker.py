from celery import Celery
from asyncio import get_event_loop
from app.core.logger import env
from app.energy.provider import energy_provider_factory
from .tasks import update_meter_from_remote, update_measurements_from_remote

celery = Celery(__name__, broker=env.broker_url, backend=env.broker_url)

loop = get_event_loop()


@celery.task(name="sync_meters", ignore_result=False)
def sync_meters(installation_id: int, name: str, key: str):
    all_remote_meters = loop.run_until_complete(
        update_meter_from_remote(installation_id, energy_provider_factory(name, key))
    )
    return f"remote meters: {len(all_remote_meters)}"


@celery.task(name="sync_installation", ignore_result=False)
def sync_installation(installation_id: int, name: str, key: str):
    return loop.run_until_complete(
        update_measurements_from_remote(
            installation_id, energy_provider_factory(name, key)
        )
    )
