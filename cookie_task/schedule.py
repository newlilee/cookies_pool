import time
from multiprocessing import Process

from log.logger import get_logger
from service.cookies_store import CookiesStore
from service.pdd_cookies_valid import PddCookieValidator
from service.tb_cookies_valid import TbCookieValidator

logger = get_logger('cookies_schedule')


class CookiePoolSchedule(object):
    @staticmethod
    def store_cookie(period=30):
        while True:
            logger.info('cookies store start.')
            try:
                CookiesStore().cookies_store('pdd')
                CookiesStore().cookies_store('tb')
                time.sleep(period)
            except Exception as e:
                logger.exception(f'store cookies e:{e}')

    @staticmethod
    def valid_cookie(period=60):
        while True:
            logger.info('cookies valid start.')
            try:
                PddCookieValidator('pdd').do_valid()
                TbCookieValidator('tb').do_valid()
                logger.info('cookies valid finished.')
                time.sleep(period)
            except Exception as e:
                logger.exception(f'valid cookies e:{e}')

    def run(self):
        # store cookie
        store_process = Process(target=CookiePoolSchedule.store_cookie)
        store_process.start()

        # valid process
        valid_process = Process(target=CookiePoolSchedule.valid_cookie)
        valid_process.start()
