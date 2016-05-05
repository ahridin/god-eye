import asyncio
from abc import ABCMeta, abstractmethod
import logging

logger = logging.getLogger(__name__)


class AbstractCheckPlugin(metaclass=ABCMeta):
    def __init__(self, loop, queue, **kwargs):
        self._loop = loop
        self._queue = queue

    @asyncio.coroutine
    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        nơi ping/download, và đo lương các thông tin
        lay cac thong tin do truyen vao ham get_result
        khong nen luu cac du lieu tim dc vao self
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError('Base_Plugin cant call')

    @asyncio.coroutine
    @abstractmethod
    def get_result(self, *args, **kwargs):
        """
        nơi implement tính toán

        :param result:
        :return:
        """
        raise NotImplementedError('Base_Plugin cant call')
