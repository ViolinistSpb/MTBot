import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger("asus_bot_logger")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    "asus_bot_logger.log", maxBytes=25_000_000, backupCount=2
)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
