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
        self._serf_client = SerfClient()
        self._snode = _snode or self._get_local_ip()
        self.network_checker = NetworkChecker(_client, _loop, _queue, self._snode)
        self.scheduler = AsyncIOScheduler()
        self._add_job(_client)


        self._list_node = []


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
            self._list_node = [x[b'Addr'].decode()
                               for x in response.body[b'Members']]
            self._list_node.remove(self._snode)

            return self._list_node.pop()


    def _get_local_ip(self):
        """
        Get `name` of node thông qua serfclient `stats`.
        Then, get ip thoong qua function `members(name)`
        :return:
        """
        name = self._serf_client.stats().body[b'agent'][b'name']
        return self._serf_client.members(name).body[b'Members'][0][b'Addr'].decode()


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
