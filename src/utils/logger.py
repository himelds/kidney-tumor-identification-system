import logging
import sys
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"

LOG_FORMAT = "[%(asctime)s] %(levelname)s %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with both console and file handlers.
    Usage:
        from src.utils.logger import get_logger
        logger = get_logger(__name__)
        logger.info("Training started")
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # Console handler — INFO and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler — DEBUG and above (full detail)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Module-level logger — import this directly for quick use
# from src.utils.logger import logger
logger = get_logger("kidney_tumor")
