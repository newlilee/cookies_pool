import logging
import os

from dynaconf import settings as dynaconf_settings

from config_center.base_consul import ConsulConfig

PROJECT_NAME = 'cookies_pool'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_LOCAL = 'local'
ENV_DEV = 'dev'
ENV_PROD = 'prod'

ENV = dynaconf_settings.current_env

if dynaconf_settings.current_env == ENV_LOCAL:
    consul_keys = ['config/spider/update,local/data']
    website_keys = ['config/spider/cookies,pdd,local/data',
                    'config/spider/cookies,tb,local/data']
    LOG_DIR = os.path.join(os.path.join(BASE_DIR, 'logs'), 'cookies_pool')
    LOG_LEVEL = logging.DEBUG
    LOG_SPIDER_LEVEL = logging.DEBUG
elif dynaconf_settings.current_env == ENV_DEV:
    consul_keys = ['config/spider/update,dev/data']
    website_keys = ['config/spider/cookies,pdd,dev/data',
                    'config/spider/cookies,tb,dev/data']
    LOG_LEVEL = logging.INFO
    LOG_SPIDER_LEVEL = logging.INFO
else:
    consul_keys = ['config/spider/update,prod/data']
    website_keys = ['config/spider/cookies,pdd,prod/data',
                    'config/spider/cookies,tb,prod/data']
    LOG_LEVEL = logging.INFO
    LOG_SPIDER_LEVEL = logging.ERROR

settings = ConsulConfig(consul_keys, False)

LOG_DIR = os.path.join(settings.LOG_DIR, 'cookies_pool')

# redis
REDIS_CONF = {
    'host': settings.REDIS_HOST,
    'port': settings.REDIS_PORT,
    'db': 0,
    'password': settings.REDIS_PWD
}
