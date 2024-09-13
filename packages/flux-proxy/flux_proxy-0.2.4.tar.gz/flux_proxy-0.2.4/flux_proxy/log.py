import logging

from rich.logging import RichHandler

format = "%(name)s: %(message)s"

logging.basicConfig(
    level="INFO",
    format=format,
    datefmt="%d/%m/%y %H:%M:%S%z",
    handlers=[RichHandler(level="NOTSET")],
)

log = logging.getLogger("fluxproxy")
