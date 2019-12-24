from flask import Flask, g

from cache.redis_client import RedisClient
from log.logger import get_logger
from log.utils import log_access

app = Flask('cookies_pool')
logger = get_logger('cookies_pool')


def get_conn(website: str):
    if not hasattr(g, website):
        setattr(g, website, eval(f'RedisClient({website})'))
    return g


@app.route('/', methods=['GET'])
@log_access
def index():
    return "Welcome to spider cookies pool."


@app.route('/spider/cookies/get/<website>/<account>', methods=['GET'])
@log_access
def delivery(website: str, account: str):
    """
    get cookie by website and account
    :param website:
    :param account:
    :return:
    """
    g = get_conn(website)
    result = getattr(g, website).get_cookie(website, f'account:{account}')
    logger.info(
        f'get cookies website={website}, account={account}, cookies={result}')
    return result


@app.route('/spider/cookies/get/random/<website>', methods=['GET'])
@log_access
def delivery_random(website: str):
    """
    random get website's cookie
    :param website:
    :return:
    """
    g = get_conn(website)
    result = getattr(g, website).get_random_cookie(website)
    logger.info(f'random get cookies website={website}, cookies={result}')
    return result


@app.route('/spider/cookies/get/balance/<website>', methods=['GET'])
@log_access
def delivery_balance(website: str):
    """
    balance get website's cookie
    :param website:
    """
    g = get_conn(website)
    result = getattr(g, website).get_balance_cookie(website)
    logger.info(f'balance get cookies website={website}, cookies={result}')
    return result


@app.route('/spider/cookies/get/count/<website>/<account>', methods=['GET'])
@log_access
def get_account_access_count(website: str, account):
    """
    get account's access count
    """
    g = get_conn(website)
    result = getattr(g, website).get_account_access_count(website, account)
    logger.info(
        f'cookies website={website}, account={account}, count={result}')
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
