import os
import sys
import logging
from time import struct_time
from datetime import datetime
from zoneinfo import ZoneInfo

jst = ZoneInfo("Asia/Tokyo")


def custom_time(*args) -> struct_time:
    return datetime.now(jst).timetuple()


def metalmental_logger(log_level=logging.INFO) -> logging.Logger:
    current_date = datetime.now(jst).strftime("%Y-%m-%d")
    log_directory = "logs"
    log_file = f"{log_directory}/{current_date}.log"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_format = "[%(asctime)s.%(msecs)03d JST] [%(levelname)s] [%(lineno)d行目] [関数名: %(funcName)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)
    formatter.converter = custom_time

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(log_level)
    file_handler = logging.FileHandler(log_file, mode="a")
    file_handler.setLevel(log_level)

    stdout_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger("metalmental_logger")
    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)
    logger.setLevel(log_level)

    return logger
