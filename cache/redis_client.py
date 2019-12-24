import json
import random

import redis

from config_center.conf import REDIS_CONF


class RedisClient(object):
    def __init__(self, website: str):
        self.host = REDIS_CONF.get('host')
        self.port = REDIS_CONF.get('port')
        self.pwd = REDIS_CONF.get('password')
        self.db = REDIS_CONF.get('db')
        self.redis = redis.StrictRedis(
            host=self.host, port=self.port, password=self.pwd, db=self.db)
        self.website = website

    def set_cookie(self, website: str, account: str, cookies: str, expire_time: int):
        """
        set website's account cookie
        :param website: pdd/tb .etc
        :param account: account
        :param cookies: cookie
        :param expire_time: cookies expire
        :return:
        """
        website = website.lower()
        account = account.lower()
        cookies_dict = {'phone': account, 'cookie': cookies}
        cache_val = json.dumps(cookies_dict)
        ret = self.redis.hsetnx(website, account, cache_val)
        if ret == 1:
            self.redis.expire(website, expire_time)
            cookie_key = f'cookies:{website}'
            self.redis.lpush(cookie_key, cache_val)
            self.redis.expire(cookie_key, expire_time)

    def get_cookie(self, website: str, account: str):
        """
        get website's cookie
        :param website: pdd/tb .etc
        :param account: account
        :return: cookie
        """
        website = website.lower()
        account = account.lower()
        count_key = f'count:{website}'
        self.redis.hincrby(count_key, account)
        return self.redis.hget(website, account)

    def get_random_cookie(self, website: str):
        """
        get website's random cookie
        :param website:
        :return:
        """
        website = website.lower()
        cookies_group = self.redis.hvals(website)
        cookies = random.choice(cookies_group)
        cookies_dict = json.loads(cookies)
        count_key = f'count:{website}'
        self.redis.hincrby(count_key, cookies_dict['phone'])
        return cookies

    def get_all_cookie(self, website: str):
        """
        get all cookie
        :param website:
        :return:
        """
        website = website.lower()
        return self.redis.lrange(f'cookies:{website}', 0, -1)

    def del_cookie(self, website: str, account: str, cookies: dict):
        """
        delete invalid cookies
        :param website:
        :param account:
        :param cookies:
        """
        website = website.lower()
        self.redis.hdel(website, account)
        cache_val = json.dumps(cookies)
        self.redis.lrem(f'cookies:{website}', 0, cache_val)

    def get_balance_cookie(self, website: str):
        """
        get balance cookie
        :param website:
        :return:
        """
        website = website.lower()
        key = f'cookies:{website}'
        cookies = self.redis.rpoplpush(key, key)
        cookies_dict = json.loads(cookies)
        count_key = f'count:{website}'
        self.redis.hincrby(count_key, cookies_dict['phone'])
        return cookies

    def get_account_access_count(self, website: str, account: str):
        """
        get website's account access count
        :param website:
        :param account:
        :return:
        """
        count_key = f'count:{website}'
        return self.redis.hget(count_key, account)
