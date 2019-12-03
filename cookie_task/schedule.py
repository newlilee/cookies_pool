import time
from multiprocessing import Process

from api.cookies_delivery import app
from service.cookies_store import CookiesStore
from service.cookies_valid import CookieValidator


class CookiePoolSchedule(object):
    @staticmethod
    def api_run():
        app.run(host='0.0.0.0', port=8090)

    @staticmethod
    def store_cookie(period=60):
        store = CookiesStore()
        while True:
            print('cookies store start.')
            try:
                store.cookies_store('pdd')
                time.sleep(period)
            except Exception as e:
                print('store cookies error:', e)

    @staticmethod
    def valid_cookie(period=30):
        while True:
            print('cookies valid start.')
            try:
                validator = CookieValidator('pdd')
                validator.do_valid()
                print('cookies valid finished.')
                del validator
                time.sleep(period)
            except Exception as e:
                print('valid cookie error:', e)

    def run(self):
        # store cookie
        store_process = Process(target=CookiePoolSchedule.store_cookie)
        store_process.start()

        # valid process
        valid_process = Process(target=CookiePoolSchedule.valid_cookie)
        valid_process.start()

        # api process
        api_process = Process(target=CookiePoolSchedule.api_run)
        api_process.start()
