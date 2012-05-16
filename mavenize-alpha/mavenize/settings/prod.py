"""Production settings and globals."""


from common import *


########## EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False
SERVER_EMAIL = 'root@localhost'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'mavenize_production',
		'USER': 'rivuze',
		'PASSWORD': '0n3t!mE!',
		'HOST': 'ec2-107-21-198-151.compute-1.amazonaws.com',
		'PORT': '5434',
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
	# Storage backend.
	'storages',

	#'djkombu',
)

#BROKER_BACKEND = 'djkombu.transport.DatabaseTransport'
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
            'level': 'ERROR',
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

########## SOCIAL-AUTH CONFIGURATION
FACEBOOK_APP_ID = '184293225012617'
FACEBOOK_API_SECRET = '122e7c7f4489c1e55c6c2589ae8e283d'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
########## END SOCIAL-AUTH CONFIGURATION

########## HAYSTACK CONFIGURATION
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://ec2-107-21-198-151.compute-1.amazonaws.com:8983/solr',
    },
}
########## END HAYSTACK CONFIGURATION

########## AMAZON S3 STORAGE BACKEND CONFIGURATION
AWS_STORAGE_BUCKET_NAME = 'mavenize-alpha'
########## END AMAZON S3 STORAGE BACKEND CONFIGURATION
