import logging

from aiohttp import web

from bublik.conf import settings
from bublik.core.management import BaseCommand


class Command(BaseCommand):
    def execute(self, loop, argv):
        app = super(Command, self).execute(loop, argv)

        # if settings.DEBUG:
        #     aiohttp_debugtoolbar.setup(app)
        #     aiohttp_autoreload.start()

        web.run_app(app, host=settings.SITE_HOST, port=settings.SITE_PORT)

    async def handle(self, loop, namespace):
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
            logging.info('Stop server begin')

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

        middlewares = [
            # session_middleware(redis_storage),
            # authentication_middleware,
        ]

        new_app = web.Application(
            loop=loop,
            middlewares=middlewares
        )

        # Routes
        # for route in routes:
        #     new_app.router.add_route(*route[:-1], name=route[3])

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
            # close_websockets,
        ]

        on_cleanup = [
            # close_redis,
            stop_end_log
        ]

        new_app.on_shutdown.extend(*on_shutdown)
        new_app.on_cleanup.extend(*on_cleanup)
        return new_app
