from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

import nexus

admin.autodiscover()
nexus.autodiscover()

urlpatterns = patterns('',
    url(r'^movies/(?P<title>[-\w]+)/$', 'movie.views.profile'),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'index.html'}, name='index'),
    url(r'^nexus/', include(nexus.site.urls)),
    url(r'', include('social_auth.urls')),
)

if settings.STATIC_MEDIA_SERVER:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': 'media'}),
)
