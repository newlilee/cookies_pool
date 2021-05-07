import json
import threading
import time

from consul import Consul
from consul import Timeout


class ConsulConfig:
    def __init__(self, keys: list, watch: bool, interval=5):
        """
        init consul client
        :param keys: consul中预先配置的key，可传多个
        :param watch: 是否监听配置变更
        :param interval: 监听间隔时间，单位：秒
        """
        self.config_dict = {}
        self.interval = interval
        if watch:
            for key in keys:
                self.consul_config_watch(key)
        else:
            for key in keys:
                self.consul_config(key)

    def consul_config_with_watch(self, key: str):
        """
        监听consul配置变更
        :param key: consul中预先配置的key
        """
        c = Consul()
        index = None
        try:
            index, data = c.kv.get(key, index=index)
            config = str(data['Value'], encoding='utf-8')
            self.config_dict = json.loads(config)
        except Timeout:
            self.config_dict[key] = None

    def consul_config_watch(self, key: str):
        """
        监听consul配置变更
        :param key: consul中预先配置的key
        """
        self.consul_config_with_watch(key)
        t = threading.Thread(target=self.consul_config_worker, args=(key,))
        t.daemon = True
        t.start()

    def consul_config_worker(self, key: str):
        """
        listen worker
        :param key: consul中预先配置的key
        """
        while True:
            time.sleep(self.interval)
            self.consul_config_with_watch(key)

    # 根据key取consul配置，监听配置变化
    # def get_consul_config_with_watch(self, key: str):
    #     return self.config_dict.get(key)

    def consul_config(self, key: str):
        """
        根据key取consul配置，不监听配置变化
        :param key: consul中预先配置的key
        """
        c = Consul()
        try:
            index = None
            index, data = c.kv.get(key, index=index)
            config = str(data['Value'], encoding='utf-8')
            self.config_dict = json.loads(config)
        except Timeout:
            return None

    def __getattr__(self, item: str):
        """
        获取配置项
        :param item: 配置项名称
        :return: 配置项值
        """
        return self.config_dict[item.lower()]
