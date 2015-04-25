# coding=utf-8
from __future__ import unicode_literals
import sys

""" Django settings for DjangoFloor project. """
from djangofloor.utils import DirectoryPath, FilePath

__author__ = 'flanker'
from os.path import join, dirname, abspath
from django.utils.translation import ugettext_lazy as _
PY2 = sys.version_info[0] == 2
# define a root path for misc. Django data (SQLite database, static files, ...)
LOCAL_PATH = abspath(join(dirname(dirname(__file__)), 'django_data'))
SERVER_NAME = 'localhost'
LOG_PATH = DirectoryPath('{LOCAL_PATH}/log')
DATA_PATH = DirectoryPath('{LOCAL_PATH}/data')
DEBUG = True
DEBUG_HELP = 'A boolean that turns on/off debug mode.'
TEMPLATE_DEBUG = False
TEMPLATE_DEBUG_HELP = 'A boolean that turns on/off template debug mode.'
ADMINS = (("admin", "admin@{SERVER_NAME}"), )
ADMINS_HELP = 'A tuple that lists people who get code error notifications.'
MANAGERS = ADMINS
MANAGERS_HELP = ('A tuple in the same format as ADMINS that specifies who should get broken link notifications '
                 'when BrokenLinkEmailsMiddleware is enabled.')
DEFAULT_FROM_EMAIL = 'admin@{SERVER_NAME}'
DEFAULT_FROM_EMAIL_HELP = 'Default email address to use for various automated correspondence from the site manager(s).'
# noinspection PyUnresolvedReferences
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': FilePath('{DATA_PATH}/database.sqlite3'),  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    },
}
DATABASES_HELP = 'A dictionary containing the settings for all databases to be used with Django.'
TIME_ZONE = 'Europe/Paris'
TIME_ZONE_HELP = 'A string representing the time zone for this installation, or None. '
BIND_ADDRESS = '127.0.0.1:9000'
BIND_ADDRESS_HELP = 'The socket (IP address:port) to bind to.'
REDIS_HOST = 'localhost'
REDIS_HOST_HELP = 'hostname of your Redis database for the multiple services using Redis (cache, Celery, websockets, sessions)'
REDIS_PORT = '6379'
REDIS_PORT_HELP = 'port of your Redis database'
THREADS = 1
THREADS_HELP = 'The number of worker threads for handling requests.'
WORKERS = 1
WORKERS_HELP = 'The number of worker process for handling requests.'
GUNICORN_PID_FILE = FilePath('{LOCAL_PATH}/run/{PROJECT_NAME}_gunicorn.pid')
GUNICORN_PID_FILE_HELP = 'A filename to use for the PID file. '
GUNICORN_ERROR_LOG_FILE = FilePath('{LOG_PATH}/gunicorn_error.log')
GUNICORN_ERROR_LOG_FILE_HELP = 'The Error log file to write to (Gunicorn).'
GUNICORN_ACCESS_LOG_FILE = FilePath('{LOG_PATH}/gunicorn_access.log')
GUNICORN_ACCESS_LOG_FILE_HELP = 'The Access log file to write to (Gunicorn).'
GUNICORN_LOG_LEVEL = 'info'
GUNICORN_LOG_LEVEL_HELP = 'The granularity of Gunicorn Error log outputs.'

USE_X_SEND_FILE = False
USE_X_SEND_FILE_HELP = 'Use the XSendFile header in Apache or LightHTTPd for sending large files'
X_ACCEL_REDIRECT = []
X_ACCEL_REDIRECT_HELP = 'Use the X-Accel-Redirect header in NGinx. List of tuples (/directory_path/, /alias_url/).'
INTERNAL_IPS = ('127.0.0.1', )
ALLOWED_HOSTS = ['127.0.0.1', '{SERVER_NAME}', ]
ALLOWED_HOSTS_HELP = 'A list of strings representing the host/domain names that this Django site can serve.'
MAX_REQUESTS = 10000
MAX_REQUESTS_HELP = 'The maximum number of requests a worker will process before restarting.'

REVERSE_PROXY_IPS = []
REVERSE_PROXY_IPS_HELP = 'List of IP addresses of the reverse proxies'
REVERSE_PROXY_TIMEOUT = 30
# Workers silent for more than this many seconds are killed and restarted.
REVERSE_PROXY_ERROR_LOG_FILE = FilePath('{LOG_PATH}/error.log')
REVERSE_PROXY_ERROR_LOG_FILE_HELP = 'Error log file to write to (Reverse proxy).'
REVERSE_PROXY_ACCESS_LOG_FILE = FilePath('{LOG_PATH}/access.log')
REVERSE_PROXY_ACCESS_LOG_FILE_HELP = 'The Access log file to write to (reverse_proxy).'
REVERSE_PROXY_SSL_KEY_FILE = None
REVERSE_PROXY_SSL_KEY_FILE_HELP = 'Key file of reverse proxy (apache/nginx). ' \
                                  'Can be set to None if the key is with the certificate.'
REVERSE_PROXY_SSL_CRT_FILE = None
REVERSE_PROXY_SSL_CRT_FILE_hep = 'SSL certificate file of reverse proxy (apache/nginx). Required if you use SSL'
REVERSE_PROXY_PORT = None  #
REVERSE_PROXY_PORT_HELP = 'Reverse proxy (apache/nginx) port (if None, defaults to 80 or 443 if you use SSL)'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-fr'
LANGUAGE_CODE_HELP = 'A string representing the language code for this installation.'
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'NEZ6ngWX0JihNG2wepl1uxY7bkPOWrTEo27vxPGlUM3eBAYfPT'
SECRET_KEY_HELP = ('A secret key for a particular Django installation. This is used to provide cryptographic signing, '
                   'and should be set to a unique, unpredictable value.')


ACCOUNT_EMAIL_VERIFICATION = None
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[{SERVER_NAME}] '
# iterable of URL of your application. 'my_app.root_urls.urls'
FLOOR_URL_CONF = None
FLOOR_INSTALLED_APPS = []
FLOOR_INDEX = None
FLOOR_PROJECT_NAME = _('DjangoFloor')

DEFAULT_GROUP_NAME = _('Users')
DEFAULT_GROUP_NAME_HELP = 'Name of the default group of newly-created users.'

EMAIL_SUBJECT_PREFIX = '[{SERVER_NAME}] '
SERVER_EMAIL = 'root@{SERVER_NAME}'
FILE_CHARSET = 'utf-8'
# The character encoding used to decode any files read from disk. This includes template files and
# initial SQL data files
FILE_UPLOAD_TEMP_DIR = None
# The directory to store data temporarily while uploading files. If None, Django will use
# the standard temporary directory for the operating system. For example, this will
# default to ‘/tmp’ on *nix-style operating systems.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True
DEFAULT_CHARSET = 'utf-8'
DEFAULT_CONTENT_TYPE = 'text/html'
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
# noinspection PyUnresolvedReferences
MEDIA_ROOT = DirectoryPath('{DATA_PATH}/media')
MEDIA_ROOT_HELP = 'Absolute filesystem path to the directory that will hold user-uploaded files.'
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
# noinspection PyUnresolvedReferences
STATIC_ROOT = DirectoryPath('{LOCAL_PATH}/static')
STATIC_ROOT_HELP = 'The absolute path to the directory where collectstatic will collect static files for deployment.'
# Additional locations of static files
STATICFILES_DIRS = (
    abspath(join(dirname(__file__), 'static')),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = ['django.contrib.staticfiles.finders.AppDirectoriesFinder',
                       'django.contrib.staticfiles.finders.FileSystemFinder',
                       'pipeline.finders.PipelineFinder', ]

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'
# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/'
WEBSOCKET_URL = '/ws/'

PIPELINE_CSS = {
    'default': {
        'source_filenames': ('bootstrap3/css/bootstrap.min.css', 'css/font-awesome.min.css', ),
        'output_filename': 'css/default.css',
        'extra_context': {
            'media': 'all',
        },
    },
}
PIPELINE_JS = {
    'default': {
        'source_filenames': ('js/jquery.min.js', 'bootstrap3/js/bootstrap.min.js', 'js/djangofloor.js', 'js/ws4redis.js', ),
        'output_filename': 'js/default.js',
    },
    'ie9': {
        'source_filenames': ('js/html5shiv.js', 'js/respond.min.js', ),
        'output_filename': 'js/ie9.js',
    }
}
# PIPELINE_ENABLED = True
# does not enable PIPELINE if DEBUG is set to True (files generated by PIPELINE are not available in DEBUG mode)

PIPELINE_MIMETYPES = (
    ('text/coffeescript', '.coffee'),
    ('text/less', '.less'),
    ('text/javascript', '.js'),
    ('text/x-sass', '.sass'),
    ('text/x-scss', '.scss')
)
# these two cmpressors are not the best ones, but are installed with DjangoFloor as dependencies
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'
PIPELINE_CSS_COMPRESSOR = 'djangofloor.middleware.RCSSMinCompressor'
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
]

MIDDLEWARE_CLASSES = ['django.middleware.cache.UpdateCacheMiddleware',
                      'django.middleware.common.CommonMiddleware',
                      'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware',
                      'django.middleware.clickjacking.XFrameOptionsMiddleware',
                      'djangofloor.middleware.IEMiddleware',
                      'djangofloor.middleware.RemoteUserMiddleware',
                      'djangofloor.middleware.BasicAuthMiddleware',
                      'djangofloor.middleware.FakeAuthenticationMiddleware',
                      'django.middleware.cache.FetchFromCacheMiddleware', ]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
DEBUG_TOOLBAR_PATCH_SETTINGS = False
TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'djangofloor.context_processors.context_base',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount', ]
if PY2:
    TEMPLATE_CONTEXT_PROCESSORS += ['ws4redis.context_processors.default', ]
ROOT_URLCONF = 'djangofloor.root_urls'

TEMPLATE_DIRS = (
    abspath(join(dirname(__file__), 'templates')),
)

# noinspection PyUnresolvedReferences
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    # 'django_admin_bootstrapped.bootstrap3',  # TODO attendre la v2.5
    # 'django_admin_bootstrapped',  # TODO attendre la v2.5
    'django.contrib.admin',
    'bootstrap3',
    'djangofloor',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'pipeline',
]
if PY2:
    INSTALLED_APPS += ['ws4redis', ]

OTHER_ALLAUTH = []
OTHER_ALLAUTH_HELP = 'Other allauth authentication providers, merely a list of allauth.socialaccount.providers.*'

BOOTSTRAP3 = {
    'jquery_url': '{STATIC_URL}js/jquery.min.js',
    'base_url': '{STATIC_URL}bootstrap3/',
    'css_url': None,
    'theme_url': None,
    'javascript_url': None,
    'horizontal_label_class': 'col-md-2',
    'horizontal_field_class': 'col-md-4',
}
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
AUTHENTICATION_HEADER = 'HTTP_REMOTE_USER'
AUTHENTICATION_HEADER_HELP = 'HTTP header corresponding to the username (when using HTTP authentication).' \
                             ' Set it to None to disable it.'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_PROXY_SSL_HEADER_HELP = 'A tuple representing a HTTP header/value combination that signifies a request is ' \
                               'secure. This controls the behavior of the request object’s is_secure() method.'
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_HOST_HELP = 'A boolean that specifies whether to use the X-Forwarded-Host header in preference to ' \
                            'the Host header. '
AUTHENTICATION_BACKENDS = [
    'djangofloor.backends.DefaultGroupRemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
FLOOR_FAKE_AUTHENTICATION_USERNAME = None
# used to fake a reverse proxy authentication for development purpose
FLOOR_FAKE_AUTHENTICATION_GROUPS = ['group1', 'group2']
# used to fake LDAP groups, added to the remotely-authenticated user

########################################################################################################################
# sessions
########################################################################################################################
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

########################################################################################################################
# caching
########################################################################################################################
# CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', }}
CACHES = {
    'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache', },
    }
CACHES_HELP = 'A dictionary containing the settings for all caches to be used with Django.'

########################################################################################################################
# django-redis-websocket
########################################################################################################################
USE_WS4REDIS = False
WS4REDIS_CONNECTION = {'host': '{REDIS_HOST}', 'port': '{REDIS_PORT}', 'db': 15, }
WS4REDIS_CONNECTION_HELP = 'If the Redis datastore uses connection settings other than the defaults.'
WS4REDIS_EXPIRE = 0
WS4REDIS_PREFIX = 'ws'
# Python dotted path to the WSGI application used by Django's runserver.
# WSGI_APPLICATION = 'djangofloor.wsgi_http.application'
WSGI_APPLICATION = 'djangofloor.wsgi_http.application'
WS4REDIS_SUBSCRIBER = 'djangofloor.df_ws4redis.Subscriber'
DF_WS_FACILITY = 'djangofloor'
########################################################################################################################
# celery
########################################################################################################################
USE_CELERY = False
CELERY_TIMEZONE = '{TIME_ZONE}'
CELERY_RESULT_EXCHANGE = '{PROJECT_NAME}_results'
CELERY_ACCEPT_CONTENT = ['json', 'yaml', 'msgpack']
BROKER_URL = 'redis://{REDIS_HOST}:{REDIS_PORT}/13'
CELERY_PID_FILE = FilePath('{LOCAL_PATH}/run/{PROJECT_NAME}_celery.pid')
CELERY_PID_FILE_HELP = 'A filename to use for the PID file. '
CELERY_APP = 'djangofloor'
CELERY_CREATE_DIRS = True
CELERY_LOG_FILE = FilePath('{LOG_PATH}/celerybeat.log')
CELERY_TASK_SERIALIZER = 'json'

########################################################################################################################
# logging
########################################################################################################################
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'djangofloor.log.FloorAdminEmailHandler',
            'min_interval': 600,
        },
        'rotating_file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': FilePath('{LOG_PATH}/django.log'),
            'maxBytes': 10000000,  # 10 MB
            'backupCount': 2,
            'encoding': 'utf-8',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': [
                'mail_admins',
                # 'rotating_file'
            ],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
LOGGING_HELP = 'A data structure containing configuration information.' \
               ' The contents of this data structure will be passed as the argument to the configuration method' \
               ' described in LOGGING_CONFIG.'

