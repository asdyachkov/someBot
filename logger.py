# logger.py
from loguru import logger
import sys
import os

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    logger.remove()  # Убираем стандартный обработчик
    logger.add("logs/bot_{time:YYYY-MM-DD}.log", rotation="500 MB", retention="10 days", level="INFO",
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
    logger.add(sys.stdout, level="INFO", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
    return logger
