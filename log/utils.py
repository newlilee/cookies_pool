import time
from functools import wraps
from urllib.parse import urlparse

from flask import request

from log.logger import get_logger, get_influx_logger

log = get_logger('cookies_pool')
influx_logger = get_influx_logger('cookies_pool')


def log_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        st = time.time()
        result = func(*args, **kwargs)
        rt = round((time.time() - st) * 1000, 3)
        path = urlparse(request.url).path

        log.info({
            'uri': request.url,
            # 'param': ast.literal_eval(request.query_string.decode('utf-8')),
            'ms': rt,
            'response': result
        })
        influx_logger.info(
            'cookies_pool,urlpath={} value={},rt={}'.format(path, 1, rt))
        return result

    return wrapper


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            result = {
                'status': 0,
                'error': str(e),
                'time': int(time.time())
            }
            log.exception(e)
            return result

    return wrapper
