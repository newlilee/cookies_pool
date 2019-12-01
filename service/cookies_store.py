import json
import re
from config_center.base_consul import ConsulConfig
from cache.redis_client import RedisClient

COOKIE_REGEX = '(.*)=([^;]*);?'


def map_to_cookie(cookie_dict: dict):
    cookie_str = ''
    for k, v in cookie_dict:
        cookie_str = f'{k}={v}; '
    length = len(cookie_str)
    if length > 0:
        cookie_str = cookie_str[0: length - 2]
    return cookie_str


def cookies_format(cookie: str):
    # cookie format
    if re.match(COOKIE_REGEX, cookie) is not None:
        return cookie
    # json
    try:
        cookie_dict = json.loads(cookie, encoding='utf-8')
        return map_to_cookie(cookie_dict)
    except json.JSONDecodeError:
        print('cookie is not json format.')
    return None


class CookiesStore(object):
    def __init__(self):
        cookie_keys = ['config/spider/cookies,pdd/data']
        self.cookie_config = ConsulConfig(cookie_keys, True)

    def cookies_store(self, website: str):
        """
        store cookie
        :param website: pdd/tb
        :return:
        """
        account_cookie = self.cookie_config.config_dict
        expire = account_cookie.get('cookie:expire')
        for account, cookies in account_cookie.items():
            if str(account).startswith('account:'):
                formatted_cookie = cookies_format(cookies)
                redis = RedisClient(website)
                redis.set_cookie(website, account, formatted_cookie, expire)


if __name__ == '__main__':
    CookiesStore().cookies_store('pdd')
