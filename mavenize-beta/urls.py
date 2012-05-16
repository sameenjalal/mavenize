from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from haystack.forms import SearchForm
from haystack.views import SearchView

import nexus

admin.autodiscover()
nexus.autodiscover()

urlpatterns = patterns('activity_feed.views',
    url(r'^$', 'index'),

    url(r'^feed/(?P<page>\d+)/$', 'activity'),
)

urlpatterns += patterns('haystack.views',
    url(r'^movies/search/$', SearchView(template='movie_search.html',
        form_class=SearchForm), name='movie-search')
)

urlpatterns += patterns('user_profile.views',
    url(r'^users/(?P<user_id>\d+)/$', 'profile', name='user-profile'),

    url(r'^users/(?P<user_id>\d+)/raves/(?P<page>\d+)/$', 'activity'),
    url(r'^users/(?P<user_id>\d+)/marks/(?P<page>\d+)/$', 'bookmarks'),
    url(r'^users/(?P<user_id>\d+)/following/(?P<page>\d+)/$', 'following'),
    url(r'^users/(?P<user_id>\d+)/followers/(?P<page>\d+)/$', 'followers'),
)

urlpatterns += patterns('movie.views',
    url(r'^movies/$', 'explore', name='movie-explore'),
    url(r'^movies/(?P<title>[-\w]+)/$', 'profile', name="movie-profile"),
    
    url(r'^movies/genres/all$', 'genres'),
    url(r'^movies/cast/all$', 'cast'),
    url(r'^movies/(?P<time_period>\w+)/(?P<page>\d+)/$', 'explore'),
)

urlpatterns += patterns('review.views',
    url(r'^movies/(?P<title>[-\w]+)/review/$', 'review',
        {'app': 'movie', 'model': 'movie'}),
    
    url(r'^disagree/(?P<review_id>\d+)/$', 'disagree'),
    url(r'^thank/(?P<review_id>\d+)/$', 'thank'),
)

urlpatterns += patterns('social_graph.views',
    url(r'^follow/(?P<user_id>\d+)/$', 'follow'),
    url(r'^unfollow/(?P<user_id>\d+)/$', 'unfollow'),
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
