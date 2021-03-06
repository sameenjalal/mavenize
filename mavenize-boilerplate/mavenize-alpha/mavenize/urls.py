from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.views.static import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mavenize.views.index', name='index'),
    url(r'^logged-in/$', 'mavenize.views.login'),
    url(r'^logout/$', 'mavenize.views.logout'),

    url(r'^movies/genre/(?P<genre>[-\w]+)/$', 'mavenize.movie.views.genre'),
    url(r'^movies/(?P<title>[-\w]+)/$', 'mavenize.movie.views.profile'),
    url(r'^movies/(?P<title>[-\w]+)/review/$', 'mavenize.review.views.review'),
    url(r'^users/(\d+)/$', 'mavenize.user_profile.views.profile'),

    url(r'^thank/(\d+)/$', 'mavenize.review.views.thank'),
    url(r'^follow/(\d+)/$', 'mavenize.social_graph.views.follow'),
    url(r'^feedback/$', 'mavenize.general_utilities.views.feedback'),

    url(r'^load/genre/(?P<genre>[-\w]+)/(?P<page>\d+)/$', 'mavenize.movie.views.load_movies'),
    url(r'^load/(?P<review_type>\w+)/(?P<title>[-\w]+)/(?P<page>\d+)/$', 'mavenize.movie.views.load_reviews'), 
    url(r'^load/(\w+)/(\d+)/$', 'mavenize.views.load_feed'),

    url('^search/', include('haystack.urls')),
    #url(r'^activity/', include('actstream.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

     url(r'^admin/', include(admin.site.urls)),
)
