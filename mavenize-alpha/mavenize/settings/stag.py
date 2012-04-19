"""Staging settings and globals."""


from common import *


########## EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = '[%s->STAGING] ' % SITE_NAME
EMAIL_USE_TLS = False
SERVER_EMAIL = 'root@localhost'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': '',						 # Or path to database file if using sqlite3.
		'USER': '',						 # Not used with sqlite3.
		'PASSWORD': '',					 # Not used with sqlite3.
		'HOST': '',						 # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',						 # Set to empty string for default. Not used with sqlite3.
	}
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
CACHES = {
	# Memcached cache. See
	# http://docs.djangoproject.com/en/1.3/topics/cache/#memcached for more
	# information.
	#'default': {
	#	'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
	#	'LOCATION': [
	#		'127.0.0.1:11211',
	#		'192.168.0.1:11211',
	#		'192.168.0.2:11211',
	#	],
	#}

	# Local memory cache. See
	# http://docs.djangoproject.com/en/1.3/topics/cache/#local-memory-caching
	# for more information.
	'default': {
		'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
		'LOCATION': SITE_NAME,
	}
}
########## END CACHE CONFIGURATION


########## CELERY CONFIGURATION
# RabbitMQ broker. See
# http://docs.celeryproject.org/en/v2.2.5/getting-started/broker-installation.html#installing-rabbitmq
#BROKER_HOST = 'localhost'
#BROKER_PORT = 5672
#BROKER_USER = 'guest'
#BROKER_PASSWORD = 'guest'
#BROKER_VHOST = '/'

INSTALLED_APPS += (
	'djkombu',
)

BROKER_BACKEND = 'djkombu.transport.DatabaseTransport'
########## END CELERY CONFIGURATION


########## LOGGING CONFIGURATION
# A sample logging configuration. The only tangible logging performed by this
# configuration is to send an email to the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for more details on
# how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'WARNING',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
	}
}
########## END LOGGING CONFIGURATION
