import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


def setup_logger() -> None:
    # Ensure the logs directory exists
    os.makedirs(".logs", exist_ok=True)

    # Set up basic logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
        handlers=[
            # Add a timed rotating file handler to log to a file
            TimedRotatingFileHandler(
                filename=f".logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
                when="midnight",
                interval=1,
                backupCount=7,  # Keep logs for 7 days
            ),
            # Add a stream handler to log to the console
            logging.StreamHandler(),
        ]
    )

    # Set the log level for aiogram.event and httpx logger to CRITICAL
    aiogram_logger = logging.getLogger("aiogram.event")
    aiogram_logger.setLevel(logging.CRITICAL)
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.CRITICAL)
