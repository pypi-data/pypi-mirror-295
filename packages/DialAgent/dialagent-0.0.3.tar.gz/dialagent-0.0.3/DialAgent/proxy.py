import redis


class ProxyManager:
    def __init__(self, **kwargs):
        self.redis_url = kwargs.get('redis_url', None)
        if self.redis_url is None:
            raise ValueError("redis_url is required")

        self.proxy_set_key = kwargs.get('proxy_set_key', 'dial-proxies')
        self.proxy_expire_key = kwargs.get('proxy_expire_key', 'dial-proxies-expire')
        self.proxy_key = kwargs.get('proxy_key', 'dial-proxies')
        self.redis_client = redis.Redis.from_url(self.redis_url, decode_responses=True)

    def add_proxy(self, name: str = None, proxy: str = None, during: int = 360000, proxy_number: int = 8):
        """
        添加代理

        :param name:
        :param proxy:
        :param during:
        :param proxy_number:
        :return:
        """
        # 将代理添加到集合中
        proxy_key = f"{self.proxy_expire_key}:{name}"
        self.redis_client.set(proxy_key, 1, ex=during)
        proxy_key = f"{self.proxy_key}:{name}"
        self.redis_client.set(proxy_key, proxy)
        for i in range(proxy_number):
            self.join_proxy_list("#".join([proxy, f"{name}#{i}"]), is_first=True)

    def delete_proxy(self, name):
        """
        删除代理

        :param name:
        :return:
        """
        proxy = self.get_use_proxy(name)
        print(f"删除代理: {proxy}")
        if proxy is not None:
            for i in range(50):
                self.redis_client.srem(self.proxy_set_key, "#".join([proxy, f"{name}#{i}"]))
        self.redis_client.delete(f"{self.proxy_expire_key}:{name}")
        self.redis_client.delete(f"{self.proxy_key}:{name}")

    def delete_all_proxy(self):
        """
        删除所有代理

        :return:
        """
        keys = self.redis_client.scan_iter(f"{self.proxy_expire_key}*")
        for key in keys:
            self.redis_client.delete(key)
        keys = self.redis_client.scan_iter(f"{self.proxy_key}*")
        for key in keys:
            self.redis_client.delete(key)
        self.redis_client.delete(self.proxy_set_key)


    def get_use_proxy(self, name):
        """
        获取使用的代理

        :param name:
        :return:
        """
        proxy_key = f"{self.proxy_key}:{name}"
        return self.redis_client.get(proxy_key)

    def check_proxy_expire(self, name):
        """
        检查代理是否过期

        :param name:
        :return:
        """
        # 判断代理是否过期
        proxy_key = f"{self.proxy_expire_key}:{name}"
        return (self.redis_client.ttl(proxy_key)) > 0

    def join_proxy_list(self, proxy: str = None, is_first: bool = False):
        """
        将代理加入到代理集合中

        :param proxy:
        :param is_first:
        :return:
        """
        name = proxy.split('#')[1]
        temp_proxy = proxy.split('#')[0]
        old_proxy = self.get_use_proxy(name)
        if (old_proxy and old_proxy == temp_proxy) or is_first:
            self.redis_client.sadd(self.proxy_set_key, proxy)
        else:
            print(f"代理已经被切换, 不加入: {proxy}")
