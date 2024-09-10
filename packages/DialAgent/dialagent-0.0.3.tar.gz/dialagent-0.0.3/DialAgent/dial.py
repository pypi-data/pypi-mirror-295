import threading
import time

from fabric2 import Connection

from proxy import ProxyManager


def get_server_info(server: str):
    """

    get server info
    :param server:
    :return:
    """
    info = server.split(':')
    if len(info) < 4:
        raise ValueError("server info error")
    return {
        'name': info[0],
        'host': info[1],
        'port': int(info[2]),
        'password': info[3],
        'proxy_number': int(info[4]) if len(info) == 5 else 8
    }


def command_run(conn, command):
    """
    run command

    :param conn:
    :param command:
    :return:
    """
    try:
        result = conn.run(command, hide=True, timeout=10)
        if result.ok:
            return result.stdout
        return None
    except Exception as e:
        return None


class Dial:
    def __init__(self, **kwargs):
        """
        server: server object [{name}:host:port:password:{代理数}]
        :param kwargs:
        """
        self.server = kwargs.get('server', None)
        if self.server is None:
            raise ValueError("server is required")
        self.nameserver = kwargs.get('nameserver', None)
        self.dial_time = kwargs.get('dial_time', 5)
        self.restart = kwargs.get('restart', True)
        self.redis_url = kwargs.get('redis_url', "redis://localhost:6379/0")

    def dial(self, server, proxyManage):
        for _ in range(10):
            server_info = get_server_info(server)
            conn = Connection(f"root@{server_info['host']}", port=server_info['port'], connect_kwargs={"password": server_info['password']})
            command_list = [
                'pppoe-stop',
                'pppoe-start',
            ]
            if self.nameserver:
                command_list.append(f'echo -e "nameserver {self.nameserver}" | tee /etc/resolv.conf > /dev/null && chmod 644 /etc/resolv.conf && cat /etc/resolv.conf')

            if self.restart:
                command_list.append('systemctl restart squid')
                command_list.append('systemctl restart tinyproxy')

            for command in command_list:
                command_run(conn, command)
            proxy = None
            for i in range(10):
                time.sleep(self.dial_time)
                proxy = command_run(conn, "curl ifconfig.me")
                if proxy:
                    break
            if proxy:
                print(f"拨号成功, 代理: {proxy}")
                proxyManage.add_proxy(name=server_info['name'], proxy=proxy, proxy_number=server_info['proxy_number'])
                break

    def check_dial(self, server, proxyManage):
        """
        校验拨号

        :param server:
        :param proxyManage:
        :return:
        """
        server_info = get_server_info(server)
        dial_name = f"{server_info['name']}"
        proxyManage.delete_all_proxy()
        for i in range(10000):
            if proxyManage.check_proxy_expire(dial_name):
                time.sleep(1)
                continue
            proxyManage.delete_proxy(dial_name)
            print(f"开始拨号: {dial_name}")
            self.dial(server, proxyManage)

    def run(self):
        proxyManage = ProxyManager(redis_url=self.redis_url)
        thread_list = []
        for server in self.server:
            print(server)
            thread_list.append(threading.Thread(target=self.check_dial, args=(server, proxyManage)))

        for thread in thread_list:
            thread.start()
