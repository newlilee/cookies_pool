from flask import Flask, g
from cache.redis_client import RedisClient

app = Flask('cookies_pool')


def get_conn(website: str):
    if not hasattr(g, website):
        setattr(g, website, eval('RedisClient' + '("' + website + '")'))
    return g


@app.route('/', methods=['GET'])
def index():
    return "Welcome to spider cookies pool."


@app.route('/spider/cookies/get/<website>/<account>', methods=['GET'])
def delivery(website: str, account: str):
    """
    get cookie by website and account
    :param website:
    :param account:
    :return:
    """
    g = get_conn(website)
    return getattr(g, website).get_cookie(website, f'account:{account}')


@app.route('/spider/cookies/get/random/<website>', methods=['GET'])
def delivery_random(website: str):
    """
    random get website's cookie
    :param website:
    :return:
    """
    g = get_conn(website)
    return getattr(g, website).get_random_cookie(website)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
