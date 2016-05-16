import asyncio
from aiohttp import web
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)

@asyncio.coroutine
def hello(request):
    return web.Response(body=b"Hello, world")

app = web.Application(debug=True)
app.router.add_route('GET', '/', hello)
web.run_app(app, port=80)
