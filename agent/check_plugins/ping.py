import logging
import asyncio
from agent.check_plugins import AbstractCheckPlugin

logger = logging.getLogger(__name__)


class Ping(AbstractCheckPlugin):
    @asyncio.coroutine
    def __call__(self, client, node_target):
        logger.info('Ping running...')

        r = yield from client.get(node_target)
        self.r = r
        text = yield from r.text()
        yield from self._queue.put(self.get_result(text))

    @asyncio.coroutine
    def get_result(self, result):
        """
        Vi du cho Dai
        :param result:
        :return:
        """
        logger.info("Ham get result: {}".format(result))
        return []

# Fast test =)))
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     with aiohttp.ClientSession() as client:
#         x = loop.run_until_complete(Ping()(client))
#     print(x)
#     print('Press Ctrl+C to exit')
#
#     # Execution will block here until Ctrl+C
#     # (Ctrl+Break on Windows) is pressed.
#     try:
#         loop.run_forever()
#     except (KeyboardInterrupt, SystemExit):
#         pass
