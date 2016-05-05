import asyncio
from abc import ABCMeta, abstractmethod
import importlib
import logging
from agent import config

logger = logging.getLogger(__name__)


class AbstractNetworkChecker(metaclass=ABCMeta):
    def __init__(self, client, loop, queue):
        self._plugins = []
        self._client = client
        self._loop = loop
        self._queue = queue

        # cai nay de duoi cung
        self._load_plugins()

    def _load_plugins(self):
        for check in config.enable_plugin:
            name = check['name']
            path = check['path']
            kwarg = check.get('kwarg', {})
            try:
                plugin = self._load_plugin(name, path, **kwarg)
            except Exception as e:
                logger.info('Error: {!r}'.format(e))
                plugin = None
                raise e

            if plugin:
                self._plugins.append(plugin)

    def _load_plugin(self, name, path, **kwarg):
        plugin = importlib.import_module(path, __name__)
        return getattr(plugin, name)(self._loop, self._queue, **kwarg)

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError('AbtractNetworkChecker cant call')

    @asyncio.coroutine
    def real_call(self, dnode):
        if self._plugins:
            cors = [plugin(self._client, dnode) for plugin in self._plugins]
            r = yield from asyncio.wait(cors, loop=self._loop, timeout=config.check_timeout)
            return r

        raise Exception('No Plugin')


class NetworkChecker(AbstractNetworkChecker):
    def __call__(self, get_node):
        logger.info('Network checker start running')
        dnode = get_node()
        self._loop.create_task(self.real_call(dnode))
        # future = asyncio.run_coroutine_threadsafe(self.real_call(dnode),
        #                                           self._loop)
        # try:
        #     # Wait for the result with a timeout
        #     result = future.result(config.check_timeout)
        # except asyncio.TimeoutError:
        #     logger.info('The coroutine took too long, cancelling the task...')
        #     future.cancel()
        # except Exception as exc:
        #     logger.info('The coroutine raised an exception: {!r}'.format(exc))
        # else:
        #     logger.info('The Checks returned: {!r}'.format(result))
        #     logger.info('Network checker end!!!')
