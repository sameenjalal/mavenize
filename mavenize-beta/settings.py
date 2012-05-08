import os
import sys
import logging, logging.handlers

import environment
import logconfig

# logic between applications, you can also share settings. Just create another
# settings file in your package and import it like so:
#
#     from comrade.core.settings import * 
#
# The top half of this settings.py file is copied from comrade for clarity. We
# use the import method in actual deployments.

# Make filepaths relative to settings.
path = lambda root,*a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))


# List of admin e-mails - we use Hoptoad to collect error notifications, so this
# is usually blank.
ADMINS = ()
MANAGERS = ADMINS

# Deployment Configuration

class DeploymentType:
    PRODUCTION = "PRODUCTION"
    DEV = "DEV"
    SOLO = "SOLO"
    STAGING = "STAGING"
    dict = {
        SOLO: 1,
        PRODUCTION: 2,
        DEV: 3,
        STAGING: 4
    }

if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DeploymentType.SOLO

def is_solo():
    return DEPLOYMENT == DeploymentType.SOLO

def is_dev():
    return DEPLOYMENT == DeploymentType.DEV

SITE_ID = DeploymentType.dict[DEPLOYMENT]

DEBUG = DEPLOYMENT != DeploymentType.PRODUCTION
STATIC_MEDIA_SERVER = is_solo() or is_dev()
TEMPLATE_DEBUG = DEBUG
SSL_ENABLED = not DEBUG

INTERNAL_IPS = ('127.0.0.1',)

# Logging

if DEBUG:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO

# Only log to syslog if this is not a solo developer server.
USE_SYSLOG = not is_solo()

# Cache Backend

CACHE_TIMEOUT = 3600
MAX_CACHE_ENTRIES = 10000
CACHE_MIDDLEWARE_SECONDS = 3600
CACHE_MIDDLEWARE_KEY_PREFIX = ''

# Don't require developers to install memcached, and also make debugging easier
# because cache is automatically wiped when the server reloads.
if is_solo() or is_dev():
    CACHE_BACKEND = ('locmem://?timeout=%(CACHE_TIMEOUT)d'
            '&max_entries=%(MAX_CACHE_ENTRIES)d' % locals())
else:
    CACHE_BACKEND = ('memcached://127.0.0.1:11211/?timeout=%(CACHE_TIMEOUT)d'
            '&max_entries=%(MAX_CACHE_ENTRIES)d' % locals())

# E-mail Server

if is_solo() or is_dev():
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'YOU@YOUR-SITE.com'
    EMAIL_HOST_PASSWORD = 'PASSWORD'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = "Mavenize Support <admin@mavenize.me>"

CONTACT_EMAIL = 'admin@mavenize.me'

# Internationalization

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
USE_I18N = False

# Testing & Coverage

# Use nosetests instead of unittest
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

COVERAGE_REPORT_HTML_OUTPUT_DIR = 'coverage'
COVERAGE_MODULE_EXCLUDES = ['tests$', 'settings$', 'urls$', 'vendor$',
        '__init__', 'migrations', 'templates', 'django', 'debug_toolbar',
        'core\.fixtures', 'users\.fixtures',]

try:
    import multiprocessing
    cpu_count = multiprocessing.cpu_count()
except ImportError:
    cpu_count = 1

NOSE_ARGS = ['--logging-clear-handlers', '--processes=%s' % cpu_count]

if is_solo():
    try:
        os.mkdir(COVERAGE_REPORT_HTML_OUTPUT_DIR)
    except OSError:
        pass

# Paths

MEDIA_ROOT = path(ROOT, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
ROOT_URLCONF = 'urls'
STATIC_ROOT = path(ROOT, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (path(ROOT, 'assets'),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Version Information

# Grab the current commit SHA from git - handy for confirming the version
# deployed on a remote server is the one you think it is.
import subprocess
GIT_COMMIT = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'],
    stdout=subprocess.PIPE).communicate()[0].strip()
del subprocess

# Database

DATABASES = {}

if 'test' in sys.argv:
    DATABASES['default'] = {
        'name': 'testdb',
        'ENGINE': 'django.db.backends.sqlite3'
    }
elif DEPLOYMENT == DeploymentType.PRODUCTION:
    DATABASES['default'] = {
        'NAME': 'boilerplate',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'your-database.com',
        'PORT': '',
        'USER': 'boilerplate',
        'PASSWORD': 'your-password'
    }
elif DEPLOYMENT == DeploymentType.DEV:
    DATABASES['default'] = {
        'NAME': 'mavenize_development',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'django',
        'PASSWORD': 'PyDjR0ck$'
    }
elif DEPLOYMENT == DeploymentType.STAGING:
    DATABASES['default'] = {
        'NAME': 'boilerplate_staging',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'your-database.com',
        'PORT': '',
        'USER': 'boilerplate',
        'PASSWORD': 'your-password'
    }
else:
    DATABASES['default'] = {
        'NAME': 'db',
        'ENGINE': 'django.db.backends.sqlite3',
        'HOST': '',
        'PORT': '',
        'USER': '',
        'PASSWORD': ''
    }

# Message Broker (for Celery)

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "celery"
BROKER_PASSWORD = "django"
BROKER_VHOST = "/"
CELERY_RESULT_BACKEND = "amqp"

# Run tasks eagerly in development, so developers don't have to keep a celeryd
# processing running.
CELERY_ALWAYS_EAGER = is_solo()
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# South

# Speed up testing when you have lots of migrations.
SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

# Logging

SYSLOG_FACILITY = logging.handlers.SysLogHandler.LOG_LOCAL0
SYSLOG_TAG = "boilerplate"

# See PEP 391 and logconfig.py for formatting help.  Each section of LOGGING
# will get merged into the corresponding section of log_settings.py.
# Handlers and log levels are set up automatically based on LOG_LEVEL and DEBUG
# unless you set them here.  Messages will not propagate through a logger
# unless propagate: True is set.
LOGGERS = {
    'loggers': {
        'boilerplate': {},
    },
}

logconfig.initialize_logging(SYSLOG_TAG, SYSLOG_FACILITY, LOGGERS, LOG_LEVEL,
        USE_SYSLOG)

# Debug Toolbar

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'EXTRA_SIGNALS': ['social_auth.signals.pre_update',
                      'social_auth.signals.socialauth_registered',
                      'bookmark.signals.state_changed']
}

# Application Settings

SECRET_KEY = '8^q6o4zyxy%p!ltd^#t)hqmb_))e5zy^nxg151f7tf)y_@%!9-'

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

# Sessions

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Middleware

middleware_list = [
    'commonware.log.ThreadRequestMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

if is_solo():
    middleware_list += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
elif is_dev():
    middleware_list += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.transaction.TransactionMiddleware',
        'commonware.middleware.SetRemoteAddrFromForwardedFor',
    ]
else:
    middleware_list += [
        'django.middleware.transaction.TransactionMiddleware',
        'commonware.middleware.SetRemoteAddrFromForwardedFor',
    ]

MIDDLEWARE_CLASSES = tuple(middleware_list)

# Templates

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

if not is_solo():
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social_auth.context_processors.social_auth_by_name_backends',
)

TEMPLATE_DIRS = (
    path(ROOT, 'templates')
)

apps_list = [
        'django.contrib.auth',
        'django.contrib.admin',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django.contrib.sessions',
        'django.contrib.markup',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'activity_feed',
        'bookmark',
        'item',
        'leaderboard',
        'notification',
        'request',
        'review',
        'social_graph',
        'user_profile',

        'movie',

        'nexus',
        'social_auth',
        'south',
        'sorl.thumbnail',
        'haystack',
]

if is_solo() or is_dev():
    apps_list += [
        'django_extensions',
        'debug_toolbar',
        'django_nose',
        'django_coverage',
    ]
INSTALLED_APPS = tuple(apps_list)

# Social Authentication

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_EXTRA_DATA = True
SOCIAL_AUTH_EXPIRATION = 'expires'

# Development Facebook application
FACEBOOK_APP_ID = '319245824782103'
FACEBOOK_API_SECRET = 'ce2645caabfeb6e234e00d3769ce1793'
FACEBOOK_EXTENDED_PERMISSIONS = ['email', 'create_event', 'publish_stream']

# User Profiles
AUTH_PROFILE_MODULE = 'user_profile.UserProfile'

# Haystack settings
HAYSTACK_CONNECTIONS = {}

if is_solo() or is_dev():
    HAYSTACK_CONNECTIONS['default'] = {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    }
