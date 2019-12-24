# -*- coding: utf-8 -*-

import requests
import time

from log.logger import get_logger
from service.base_cookies_valid import CookieValid

logger = get_logger('tb_cookies_valid')


class TbCookieValidator(CookieValid):
    def __init__(self, website: str):
        self.website = website
        CookieValid.__init__(self, website)

    @staticmethod
    def map_to_cookie(cookie_dict: dict):
        cookie_str = ''
        for k, v in cookie_dict.items():
            cookie_str += f'{k}={v}; '
        length = len(cookie_str)
        if length > 0:
            cookie_str = cookie_str[0: length - 2]
        return cookie_str

    def update_consul(self, key: str, value: str):
        config_dict = self.cookie_config.config_dict
        config_dict.update({key: value})
        self.cookie_config.consul_config_set(
            'config/spider/cookies,tb,prod/data', config_dict)

    def validator(self, account_cookies: dict):
        valid_url = self.valid_url
        try:
            account = account_cookies['phone']
            cookies = account_cookies['cookie']
            cookie_data = CookieValid.cookie_to_map(cookies)
            response = requests.get(
                valid_url, cookies=cookie_data, timeout=10, allow_redirects=False)
            # 判断cookie失效规则
            if response.status_code == 200 or response.status_code == 302:
                valid_key = f'{self.website}:account:{account}'
                user_id = cookie_data.get('unb')
                if response.content is not None:
                    content = str(response.content, encoding='utf-8')
                    if content.count(user_id) < 1:
                        self.redis.del_cookie(
                            self.website, account, account_cookies)
                        logger.info(
                            f'website:{self.website}, account:{account}, cookies invalid deleted.')
                        new_cookies = self.gen_new_cookies(account, user_id)
                        if new_cookies:
                            self.update_consul(valid_key, new_cookies)
                            logger.info(
                                f'website:{self.website}, account:{account}, updated.')
                    else:
                        logger.info(
                            f'website:{self.website}, account:{account}, cookies valid')
                else:
                    self.redis.del_cookie(self.website, account, cookies)
                    logger.info(
                        f'website:{self.website}, account:{account}, cookies invalid deleted.')
                    new_cookies = self.gen_new_cookies(account, user_id)
                    if new_cookies:
                        self.update_consul(valid_key, new_cookies)
                        logger.info(
                            f'website:{self.website}, account:{account}, updated.')
        except requests.ConnectionError as e:
            logger.exception(f'valid cookie error:{e}')

    def gen_new_cookies(self, account: str, user_id):
        """
        generate new cookies
        :param account:
        :param user_id:
        :return: new cookies
        """
        time.sleep(30)
        generate_cookies_url = self.cookie_config.config_dict.get(
            f'{self.website}:generate:url')
        pwd = self.cookie_config.config_dict.get(
            f'{self.website}:pwd:{account}')
        params = {
            'account': account,
            'password': pwd
        }
        response = requests.post(generate_cookies_url, params, timeout=30)
        if response.status_code == 200 and response.content:
            data_json = response.json()
            standard_cookies = TbCookieValidator.map_to_cookie(
                data_json['cookies'])
            if self.valid_cookies(standard_cookies, user_id):
                logger.info(
                    f'website:{self.website} generate new cookies={standard_cookies}')
                return standard_cookies
        return None

    def valid_cookies(self, cookies: str, user_id):
        valid_url = self.valid_url
        cookie_data = CookieValid.cookie_to_map(cookies)
        response = requests.get(
            valid_url, cookies=cookie_data, timeout=10, allow_redirects=False)
        if response.status_code == 200:
            content = str(response.content, encoding='utf-8')
            return content.count(user_id) >= 1
        return False


if __name__ == '__main__':
    TbCookieValidator('tb').do_valid()
