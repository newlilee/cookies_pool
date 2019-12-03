import requests

from cache.redis_client import RedisClient
from config_center.base_consul import ConsulConfig


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


class CookieValid(object):
    def __init__(self, website: str):
        self.website = website
        keys = ['config/spider/cookies,pdd/data']
        self.consul_client = ConsulConfig(keys, True)
        self.valid_url = self.consul_client.__getattr__('cookie:valid:url')
        self.redis = RedisClient(website)

    def validator(self, account: str, cookies: str):
        raise NotImplementedError

    def do_valid(self):
        website_cookies = self.redis.get_all_cookie(self.website)
        for account, cookies in website_cookies.items():
            account = str(account, encoding='utf-8')
            account = account.rsplit(':')[1]
            cookies = str(cookies, encoding='utf-8')
            self.validator(account, cookies)


class CookieValidator(CookieValid):
    def __init__(self, website: str):
        self.website = website
        CookieValid.__init__(self, website)

    def validator(self, account: str, cookies: str):
        valid_url = self.valid_url
        try:
            cookie_data = cookie_to_map(cookies)
            response = requests.get(
                valid_url, cookies=cookie_data, timeout=10, allow_redirects=False)
            # 判断cookie失效规则
            if response.status_code == 200:
                if response.content is not None:
                    content = str(response.content, encoding='utf-8')
                    uid = self.consul_client.__getattr__(f'uid:{account}')
                    if content.find(uid) == -1:
                        print('account:', account, 'cookies invalid')
                        self.redis.del_cookie(self.website, account)
                    else:
                        print('account:', account, 'cookies valid')
                else:
                    print('account:', account, 'cookies invalid')
                    self.redis.del_cookie(self.website, account)
                # TODO: 重新生成此账号的cookie
        except requests.ConnectionError as e:
            print('valid cookie error:', e)


if __name__ == '__main__':
    CookieValidator('pdd').do_valid()
