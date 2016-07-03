import asyncio

import aiohttp_autoreload
import jinja2
import aioredis
import aiohttp_jinja2

import aiohttp_debugtoolbar

from collections import defaultdict

from aiohttp import web
from aiohttp_session import session_middleware

from _base.routes import routes
from _base import settings
from account.middleware import authentication_middleware
from account.storage import DjangoRedisStorage


async def get_app(current_loop, ssl_context=None):
    # async def get_redis():
    #     pool = await aioredis.create_pool(
    #         (settings.REDIS_HOST, settings.REDIS_PORT),
    #         db=settings.REDIS_DB, password=settings.REDIS_PASSWORD
    #     )
    #
    #     storage = DjangoRedisStorage(
    #         pool,
    #         cookie_name=settings.SESSION_COOKIE_NAME,
    #         domain=settings.SESSION_COOKIE_DOMAIN,
    #         max_age=settings.SESSION_COOKIE_AGE,
    #     )
    #     return pool, storage

    def stop_begin_log(current_app):
        settings.log.info('Stop server begin')

    # async def close_redis(current_app):
    #     settings.log.info('Closing redis connection')
    #     await current_app['redis_pool'].clear()
    #
    # async def close_websockets(current_app):
    #     await close_websockets_tree(current_app['websockets'])
    #
    # async def close_websockets_tree(websockets):
    #     if isinstance(websockets, dict):
    #         for channel in websockets.values():
    #             return await close_websockets_tree(channel)
    #
    #     while websockets:
    #         ws = websockets.pop()
    #         await ws.close(message='Server shutdown')

    def stop_end_log(current_app):
        settings.log.info('Stop server end')

    # redis_pool, redis_storage = await get_redis()

    # Middlewares
    middlewares = [
        # session_middleware(redis_storage),
        # authentication_middleware,
    ]

    new_app = web.Application(
        loop=current_loop,
        middlewares=middlewares
    )

    # Routes
    for route in routes:
        new_app.router.add_route(*route[:-1], name=route[3])

    # Static and media server
    # if settings.DEBUG:
        # new_app.router.add_static('/static', 'frontend/chat/static', name='static')

    # Cache
    # new_app['redis_pool'] = redis_pool

    # WebSockets
    # new_app['websockets'] = {
    #     'messages': defaultdict(list),
    #     'rooms': {
    #         'camp': defaultdict(list),
    #         'party': defaultdict(list),
    #         'partyleader': defaultdict(list),
    #     }
    # }

    # Template engine
    # aiohttp_jinja2.setup(new_app, loader=jinja2.FileSystemLoader('frontend/chat/templates'))

    on_shutdown = [
        stop_begin_log,
        close_websockets,
    ]

    on_cleanup = [
        close_redis,
        stop_end_log
    ]

    new_app.on_shutdown.extend(*on_shutdown)
    new_app.on_cleanup.extend(*on_cleanup)

    return new_app


if __name__ == '__main__':
    debug = True
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(get_app(loop))

    if settings.DEBUG:
        aiohttp_debugtoolbar.setup(app)
        aiohttp_autoreload.start()

    web.run_app(app)
