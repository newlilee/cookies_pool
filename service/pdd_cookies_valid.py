import requests

from log.logger import get_logger
from service.base_cookies_valid import CookieValid

logger = get_logger('pdd_cookies_valid')


class PddCookieValidator(CookieValid):
    def __init__(self, website: str):
        self.website = website
        CookieValid.__init__(self, website)

    def update_consul(self, key: str):
        config_dict = self.cookie_config.config_dict
        config_dict.update({key: False})
        self.cookie_config.consul_config_set(
            'config/spider/cookies,pdd,dev/data', config_dict)

    def validator(self, account_cookies: dict):
        valid_url = self.valid_url
        try:
            account = account_cookies['phone']
            cookies = account_cookies['cookie']
            cookie_data = CookieValid.cookie_to_map(cookies)
            response = requests.get(
                valid_url, cookies=cookie_data, timeout=10, allow_redirects=False)
            # 判断cookie失效规则
            if response.status_code == 200:
                valid_key = f'{self.website}:valid:{account}'
                if response.content is not None:
                    content = str(response.content, encoding='utf-8')
                    if content.count('goodsID') < 1:
                        self.redis.del_cookie(
                            self.website, account, account_cookies)
                        logger.info(
                            f'website:{self.website}, account:{account}, cookies invalid deleted.')
                        self.update_consul(valid_key)
                        logger.info(
                            f'website:{self.website}, account:{account}, unavailable.')
                    else:
                        logger.info(
                            f'website:{self.website}, account:{account}, cookies valid')
                else:
                    self.redis.del_cookie(self.website, account, cookies)
                    logger.info(
                        f'website:{self.website}, account:{account}, cookies invalid deleted.')
                    self.update_consul(valid_key)
                    logger.info(
                        f'website:{self.website}, account:{account}, unavailable.')
                # TODO: 重新生成此账号的cookie
        except requests.ConnectionError as e:
            logger.exception(f'valid cookie error:{e}')


if __name__ == '__main__':
    PddCookieValidator('pdd').do_valid()
