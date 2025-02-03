import logging
from logging.handlers import RotatingFileHandler

# Создаём логгер
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

# Создаём обработчик с ротацией файлов
handler = RotatingFileHandler(
    "my_logger.log", maxBytes=50_000_000, backupCount=2
)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
