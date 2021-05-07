import json

from cache.redis_client import RedisClient
from config_center.base_consul import ConsulConfig


class CookieValid:
    def __init__(self, website: str):
        self.website = website
        # website_keys = ['config/spider/cookies,pdd,dev/data',
        #                 'config/spider/cookies,tb,dev/data']
        website_keys = ['config/spider/cookies,tb,prod/data']
        self.cookie_config = ConsulConfig(website_keys, True)
        self.valid_url = self.cookie_config.__getattr__(
            f'{website}:cookie:valid:url')
        self.redis = RedisClient(website)

    def validator(self, account_cookies: dict):
        raise NotImplementedError

    def do_valid(self):
        website_cookies = self.redis.get_all_cookie(self.website)
        for ele in website_cookies:
            account_cookies = json.loads(ele)
            self.validator(account_cookies)

    @staticmethod
    def cookie_to_map(cookies: str):
        cookie_dict = {}
        cookies_group = cookies.split(';')
        for ele in cookies_group:
            cookie_pair = ele.split('=', 1)
            if len(cookie_pair) == 2:
                name = cookie_pair[0].strip()
                value = cookie_pair[1].strip()
                cookie_dict[name] = value
        return cookie_dict
