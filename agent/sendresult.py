import asyncio
import logging
from influxdb import InfluxDBClient
from agent import config

logger = logging.getLogger(__name__)


class SendResult(object):

    def __init__(self, queue):
        self._queue = queue
        self.client = InfluxDBHandler.get_client()

    @asyncio.coroutine
    def __call__(self):
        """
        _queue chua coroutine cua

        :return:
        """
        while True:
            cor_result = yield from self._queue.get()
            result = yield from cor_result
            logger.info(result)
            try:
                logger.info(
                    "Connected to InfluxDB. Writing data to database...")
                self.client.write_points(result)
            except:
                logging.exception(
                    "We get some problems when write points to database")


class InfluxDBHandler(object):

    def __init__(self):
        self.host = config.INFLUXDB_HOST
        self.port = config.INFLUXDB_PORT
        self.username = config.INFLUXDB_USERNAME
        self.password = config.INFLUXDB_PASSWORD
        self.database = config.INFLUXDB_DBNAME

    def get_client(self):
        client = None
        try:
            logging.info("Connecting to InfluxDB...")
            client = InfluxDBClient(self.host, self.port, self.username,
                                    self.password, self.database)
        except:
            logging.exception("Connect to InfuxDB is failed!")
        return client
