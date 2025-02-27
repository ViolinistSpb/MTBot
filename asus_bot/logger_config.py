import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger("asus_bot_logger")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    "asus_bot_logger.log", maxBytes=50_000_000, backupCount=2
)
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%m %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
