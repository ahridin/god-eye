from agent.check_plugins.download_speed import Download
import asyncio
import aiohttp
import unittest
import json


class TestFirstBytePlugin(unittest.TestCase):

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
            download = Download(self.loop, queue, 'public_ip')
            with aiohttp.ClientSession(loop=self.loop) as client:
                yield from download(client, 'www.dockerbook.com/TheDockerBook_sample.pdf')
            cor_result = yield from queue.get()
            result = yield from cor_result
            self.assertIsInstance(result, list)

        self.loop.run_until_complete(go())
    