from asyncio import get_event_loop
from celery import Celery

from app.core.settings import env
from app.energy.tasks import update_measurements, update_meters


celery = Celery(__name__, broker=env.broker_url, backend=env.broker_url)
loop = get_event_loop()

@celery.task(name="sync_meters", ignore_result=False)
def sync_meters(installation_id: int, name: str, key: str):
    return loop.run_until_complete(update_meters(installation_id, name, key))

@celery.task(name="sync_installation", ignore_result=False)
def sync_installation(installation_id: int, name: str, key: str):
    return loop.run_until_complete(update_measurements(installation_id, name, key))

