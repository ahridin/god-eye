import logging
import asyncio
from agent.check_plugins import AbstractCheckPlugin

# Do khong biet dung thu vien asyncio ntn ca nen em dung thu vien request
# python
import requests
import sys
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class FirstByte(AbstractCheckPlugin):

    @asyncio.coroutine
    def __call__(self, client, dnode):
        logger.info('Caculating time for download first byte...')
        dnode = 'http://{}'.format(dnode)
        r = requests.get(dnode, stream=True)
        if total_length is None:
            logger.info("empty file!")
        else:
            start_chunk = time.clock()
            for chunk in r.iter_content(1024):  # 1kB1024 1MB 1048576
                end_chunk = time.clock()
                break

            delta = end_chunk - start_chunk  # time to first byte
            yield from self._queue.put(self.get_result(dnode, delta))
            
    @asyncio.coroutine
    def get_result(self, url, delta):
        """
        download and processing data
        """
        logger.info("Caculation time for download first byte done!")
        return [self.output([self._snode, url, str(datetime.now()), delta])]

    def output(self, my_array):
        return {
            "measurement": "time_to_first_byte",
            "tags": {
                "snode": "{}".format(my_array[0]),
                "dnode": "{}".format(my_array[1])
            },
            "time": "{}".format(my_array[2]),
            "fields": {
                "value": my_array[3]
            }
        }
