import logging

from uvicorn.logging import ColourizedFormatter

from app.settings.configuration import configuration

log = logging.getLogger()

log.setLevel(configuration.app_log_level)

console_handler = logging.StreamHandler()
console_handler.setFormatter(
    ColourizedFormatter("%(levelprefix)s %(asctime)s | %(message)s")
)

log.addHandler(console_handler)
