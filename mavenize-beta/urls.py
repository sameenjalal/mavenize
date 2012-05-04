from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

import nexus

admin.autodiscover()
nexus.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'activity_feed.views.index'),
    url(r'^users/(?P<user_id>\d+)/$', 'user_profile.views.profile',
        name='user-profile'),
    url(r'^movies/$', 'movie.views.explore'),
    url(r'^movies/(?P<title>[-\w]+)/$', 'movie.views.profile',
        name="movie-profile"),
    url(r'^movies/(?P<title>[-\w]+)/review/$', 'review.views.review',
        {'app': 'movie', 'model': 'movie'}),

    url(r'^users/(?P<user_id>\d+)/raves/(?P<page>\d+)/$', 'user_profile.views.activity'),
    url(r'^movies/genres/all$', 'movie.views.genres'),
    url(r'^movies/cast/all$', 'movie.views.cast'),
    url(r'^movies/(?P<time_period>\w+)/(?P<page>\d+)/$', 'movie.views.explore'),
    url(r'^disagree/(?P<review_id>\d+)/$', 'review.views.disagree'),
    url(r'^thank/(?P<review_id>\d+)/$', 'review.views.thank'),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^nexus/', include(nexus.site.urls)),
    url(r'', include('social_auth.urls')),
)

if settings.STATIC_MEDIA_SERVER:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': 'media'}),
)
