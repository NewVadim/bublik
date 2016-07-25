DEBUG = True

MIDDLEWARE_CLASSES = (
    'account.middleware.AuthenticationMiddleware'
)

DATABASES = {
    'default': {
        'engine': 'django.db.backends.postgresql_psycopg2',
        'orm': 'peewee',
        'database': 'artek_plus',
        'user': 'postgres',
        'password': '1111',
        'host': '192.168.0.56',
        'port': '5432',
    }
}

TIME_ZONE = 'UTC'

SITE_PORT = 8080

SITE_HOST = '0.0.0.0'

SOCKETS = {}

# SESSION_COOKIE_NAME = 'sessionid'
# SESSION_COOKIE_DOMAIN = '.artek.ru'
# SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
# SESSION_KEY_PREFIX = 'cache:{redis_db}:django.contrib.sessions.cache'.format(redis_db=REDIS_DB)
# AUTH_SESSION_KEY = '_auth_user_id'
