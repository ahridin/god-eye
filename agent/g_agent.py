import sys
import logging
import asyncio
from agent import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from agent.networkchecker import NetworkChecker
import aiohttp
# from datetime import datetime
from agent.sendresult import SendResult
from serfclient.client import SerfClient


logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("apscheduler.executors.default").setLevel("ERROR")


# @asyncio.coroutine
# def tick(dsf):
#     print('Tick! The time is: %s' % datetime.now())
#

class Agent(object):
    def __init__(self, _client, _loop, _queue, _snode=None):
        """

        :param _client:
        :param _loop:
        :param _queue:
        :param _snode: ip of current node
        """
        self._loop = _loop
        self._queue = _queue
        self.network_checker = NetworkChecker(_client, _loop, _queue)
        self.scheduler = AsyncIOScheduler()
        self._add_job(_client)

        # TODO[techbk] Serf có cung cấp hàm để get local ip không? Hiện chưa tìm thấy.
        self._serf_client = SerfClient()
        # hard list node for v0.0.1
        # self._hard_list_node = ['http://127.0.0.1:8080/',
        #                         'http://httpbin.org/get']
        self._list_node = []
        self._snode = 'http://{}'.format(_snode or self._get_local_ip())

    def _add_job(self, _client):
        # self.scheduler.add_job(tick, 'interval',
        # seconds=config.check_interval, args=[_client,])
        # self.scheduler.add_job(self._loop.call_soon_threadsafe,
        # 'interval', seconds=config.check_interval,
        #  args=(self.network_checker,))
        self.scheduler.add_job(self.network_checker, 'interval',
                               seconds=config.check_interval,
                               args=(self._get_node,))

    def _get_node(self):
        """
        De quy cho mau =)))
        :return:
        """
        try:
            return self._list_node.pop()
        except IndexError:
            # self._list_node = self._hard_list_node[:]
            response = self._serf_client.members()
            self._list_node = ['http://{}'.format(x[b'Addr'].decode())
                               for x in response.body[b'Members']]
            self._list_node.remove(self._snode)

            return self._list_node.pop()


    # TODO[techbk]: add config xác định rõ interface.
    def _get_local_ip(self, ifname = b'eth0'):
        """
        Ở đây đang mặc định local_ip thuộc interface eth0
        :return:
        """
        import socket
        import fcntl
        import struct

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    queue = asyncio.Queue(loop=loop)

    # khoi tao Task send_result
    send_result = SendResult(queue)
    asyncio.async(send_result())

    with aiohttp.ClientSession() as client:
        _agent = Agent(client, loop, queue)
        _agent.scheduler.start()
        print('Press Ctrl+C to exit')
        try:
            loop.run_forever()
        except (KeyboardInterrupt, SystemExit):
            pass
