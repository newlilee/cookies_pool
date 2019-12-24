import logging
import os
from logging import handlers

from config_center.conf import LOG_DIR, LOG_LEVEL

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def get_logger(log_name: str, when='D', backup_count=5):
    formatter = logging.Formatter(
        "[%(asctime)s %(filename)s %(funcName)s line:%(lineno)d %(levelname)s]: %(message)s")

    logger = logging.getLogger(log_name)
    logger.setLevel(LOG_LEVEL)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    filename = os.path.join(LOG_DIR, f'{log_name}.log')
    th = handlers.TimedRotatingFileHandler(
        filename=filename,
        when=when,
        backupCount=backup_count,
        encoding='utf-8'
    )
    th.setFormatter(formatter)
    logger.addHandler(th)
    return logger


def get_influx_logger(logger_name, when='D', backup_count=2):
    """
    :param logger_name:
    :param when:
    :param backup_count:
    :return:
    """
    logger_name = "influx_{}".format(logger_name.lower())
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    log_name = os.path.join(LOG_DIR, "{}.log".format(logger_name))

    rotate_handler = handlers.TimedRotatingFileHandler(
        filename=log_name,
        when=when,
        backupCount=backup_count,
        encoding='utf-8'
    )
    rotate_handler.setLevel(logging.INFO)
    logger.addHandler(rotate_handler)
    return logger
