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


class Download(AbstractCheckPlugin):

    @asyncio.coroutine
    def __call__(self, client, dnode):
        logger.info('Test download speed :  running...')
        start = time.clock()
        r = requests.get('http://{}'.format(dnode), stream=True)
        total_length = int(r.headers.get('content-length'))
        if total_length is None:
            logger.error("Empty file!")
        else:
            array_speed = []
            start_chunk = time.clock()
            for chunk in r.iter_content(1024):  # 1kB1024 1MB 1048576
                end_chunk = time.clock()
                delta = end_chunk - start_chunk
                start_chunk = end_chunk
                if delta <= 0:
                    break
                else:
                    array_speed.append(1//delta)  # kB / s

            end = time.clock()
            yield from self._queue.put(self.get_result(dnode, start, end, total_length, array_speed))

    @asyncio.coroutine
    def get_result(self, url, start, end, total_length, array_speed):
        """
        download and processing data
        """
        download_speed = total_length // (time.clock() - start)
        accelerationS = self.acceleration(array_speed)
        mean_deviationS = self.mean_deviation(array_speed, download_speed)
        logger.info("Test download speed done!")
        #TODO Bỏ time, để kiểm tra xem db có ghi đc dữ liệu hay chưa
        return [self.output([self._snode, url, datetime.now(), download_speed, mean_deviationS, accelerationS])]

    def acceleration(self, array_speed):
        if len(array_speed) == 0:
            return 0
        speed_before = array_speed[0]
        for speed in array_speed:
            if speed < speed_before:
                break
            else:
                speed_before = speed

        return speed_before - array_speed[0]

    def mean_deviation(self, array_speed, download_speed):
        if len(array_speed) == 0:
            return 0
        sum = 0
        for speed in array_speed:
            sum += abs(speed - download_speed)

        return sum//len(array_speed)

    def output(self, my_array):
        return {
            "measurement": "download_speed",
            "tags": {
                "snode": "{}".format(my_array[0]),
                "dnode": "{}".format(my_array[1])
            },
            # "time": "{}".format(my_array[2]),
            "fields": {
                "speed": my_array[3],
                "mean_deviation": my_array[4],
                "acceleration": my_array[5]
            }
        }
