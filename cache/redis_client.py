import random
import redis
from config_center.base_consul import ConsulConfig


class RedisClient(object):
    def __init__(self, website: str):
        keys = ['config/spider/cookies,dev/data']
        consul_client = ConsulConfig(keys, False)
        self.host = consul_client.__getattr__('cookie.pool.host')
        self.port = consul_client.__getattr__('cookie.pool.port')
        self.pwd = consul_client.__getattr__('cookie.pool.pwd')
        self.db = consul_client.__getattr__('cookie.pool.db')
        self.redis = redis.StrictRedis(
            host=self.host, port=self.port, password=self.pwd, db=self.db)
        self.website = website

    def set_cookie(self, website: str, account: str, value: str, expire_time: int):
        """
        set website's account cookie
        :param website: pdd/tb .etc
        :param account: account
        :param value: cookie
        :param expire_time: cookies expire
        :return:
        """
        website = website.lower()
        account = account.lower()
        self.redis.hset(website, account, value)
        self.redis.expire(website, expire_time)

    def get_cookie(self, website: str, account: str):
        """
        get website's cookie
        :param website: pdd/tb .etc
        :param account: account
        :return: cookie
        """
        website = website.lower()
        account = account.lower()
        return self.redis.hget(website, account)

    def get_random_cookie(self, website: str):
        """
        get website's random cookie
        :param website:
        :return:
        """
        website = website.lower()
        cookies = self.redis.hvals(website)
        return random.choice(cookies)

    def get_all_cookie(self, website: str):
        """
        get all cookie
        :param website:
        :return:
        """
        website = website.lower()
        return self.redis.hgetall(website)

    def del_cookie(self, website: str, account: str):
        """
        delete invalid cookies
        :param website:
        :param account:
        """
        website = website.lower()
        self.redis.hdel(website, account)
