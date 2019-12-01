import time
from multiprocessing import Process

from service.cookies_valid import CookieValidator
from service.cookies_store import CookiesStore
from api.cookies_delivery import app


class CookiePoolSchedule(object):
    @staticmethod
    def api_run():
        app.run(host='0.0.0.0', port=8090)

    @staticmethod
    def store_cookie():
        store = CookiesStore()
        store.cookies_store('pdd')

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
        # api process
        api_process = Process(target=CookiePoolSchedule.api_run)
        api_process.start()

        # store cookie
        store_process = Process(target=CookiePoolSchedule.store_cookie)
        store_process.start()

        # valid process
        valid_process = Process(target=CookiePoolSchedule.valid_cookie)
        valid_process.start()
