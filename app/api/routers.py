from fastapi import APIRouter

from app.api.controllers.auth import router as auth
from app.api.controllers.task import router as task
from app.api.controllers.channel import router as channel
from app.api.controllers.installation import router as installation
from app.api.controllers.measurements import router as measurements
from app.api.controllers.meter import router as meter
from app.api.controllers.user import router as user



api_router = APIRouter(prefix="/api")

api_router.include_router(auth, prefix="/auth", tags=["Auth"])

api_router.include_router(user, prefix="/user", tags=["User"])
api_router.include_router(installation, prefix="/installation", tags=["Installation"])
api_router.include_router(meter, prefix="/meter", tags=["Meter"])
api_router.include_router(channel, prefix="/channel", tags=["Channel"])
api_router.include_router(measurements, prefix="/measurements", tags=["Measurements"])  # pylint: disable=line-too-long

api_router.include_router(task, prefix="/task", tags=["Tasks"])
