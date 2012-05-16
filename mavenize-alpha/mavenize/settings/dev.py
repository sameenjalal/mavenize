"""Development settings and globals."""


from common import *
from os.path import join, normpath


########## DEBUG CONFIGURATION
DEBUG = True
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mavenize_dev',
        'USER': 'django',
        'PASSWORD': 'PyDjR0ck$',
        'HOST': 'localhost',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
	}
}
########## END CACHE CONFIGURATION


########## DJANGO-DEBUG-TOOLBAR CONFIGURATION
MIDDLEWARE_CLASSES += (
	'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
	'debug_toolbar',
)

# IPs allowed to see django-debug-toolbar output.
INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
	# If set to True (default), the debug toolbar will show an intermediate
	# page upon redirect so you can view any debug information prior to
	# redirecting. This page will provide a link to the redirect destination
	# you can follow when ready. If set to False, redirects will proceed as
	# normal.
	#'INTERCEPT_REDIRECTS': False,

	# If not set or set to None, the debug_toolbar middleware will use its
	# built-in show_toolbar method for determining whether the toolbar should
	# show or not. The default checks are that DEBUG must be set to True and
	# the IP of the request must be in INTERNAL_IPS. You can provide your own
	# method for displaying the toolbar which contains your custom logic. This
	# method should return True or False.
	#'SHOW_TOOLBAR_CALLBACK': None,

	# An array of custom signals that might be in your project, defined as the
	# python path to the signal.
	#'EXTRA_SIGNALS': [],

	# If set to True (the default) then code in Django itself won't be shown in
	# SQL stacktraces.
	#'HIDE_DJANGO_SQL': True,

	# If set to True (the default) then a template's context will be included
	# with it in the Template debug panel. Turning this off is useful when you
	# have large template contexts, or you have template contexts with lazy
	# datastructures that you don't want to be evaluated.
	#'SHOW_TEMPLATE_CONTEXT': True,

	# If set, this will be the tag to which debug_toolbar will attach the debug
	# toolbar. Defaults to 'body'.
	#'TAG': 'body',
}
########## END DJANGO-DEBUG-TOOLBAR CONFIGURATION


########## CELERY CONFIGURATION
INSTALLED_APPS += (
	#'djkombu',
)

#BROKER_BACKEND = 'djkombu.transport.DatabaseTransport'
########## END CELERY CONFIGURATION

########## SOCIAL-AUTH CONFIGURATION
FACEBOOK_APP_ID = '319245824782103'
FACEBOOK_API_SECRET = 'ce2645caabfeb6e234e00d3769ce1793'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
########## END SOCIAL-AUTH CONFIGURATION

########## HAYSTACK CONFIGURATION
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr',
    },
}
########## END HAYSTACK CONFIGURATION

########## AMAZON S3 STORAGE BACKEND CONFIGURATION
AWS_STORAGE_BUCKET_NAME = 'mavenize-dev'
########## END AMAZON S3 STORAGE BACKEND CONFIGURATION
