from agent.check_plugins.ping import Ping
import asyncio
import aiohttp
import unittest
import json


class TestPingPlugin(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.stop()
        self.loop.run_forever()
        self.loop.close()

    def test_get_result(self):

        @asyncio.coroutine
        def go():
            queue = asyncio.Queue(loop=self.loop)
            ping = Ping(self.loop, queue)
            with aiohttp.ClientSession(loop=self.loop) as client:
                yield from ping(client, 'http://httpbin.org/get')
            cor_result = yield from queue.get()
            result = yield from cor_result
            result = json.loads(result)
            self.assertIsInstance(result, dict)
            self.assertEqual(result['url'], 'http://httpbin.org/get')

        self.loop.run_until_complete(go())