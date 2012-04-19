from django.contrib import admin
from django.conf.urls.defaults import include, patterns, url
from django.conf import settings


admin.autodiscover()
urlpatterns = patterns('',
    # Index and authentication.
    url(r'^$', 'apps.general_utilities.views.index', name='index'),
    url(r'^logged-in/$', 'apps.general_utilities.views.login'),
    url(r'^logout/$', 'apps.general_utilities.views.logout'),

    # Genre, movie, and user profiles.
    url(r'^movies/genre/(?P<genre>[-\w]+)/$', 'apps.movie.views.genre'),
    url(r'^movies/(?P<title>[-\w]+)/$', 'apps.movie.views.profile'),
    url(r'^users/(\d+)/$', 'apps.user_profile.views.profile'),

    # Thank, follow, feedback, and review actions.
    url(r'^thank/(\d+)/$', 'apps.review.views.thank'),
    url(r'^follow/(\d+)/$', 'apps.social_graph.views.follow'),
    url(r'^feedback/$', 'apps.general_utilities.views.feedback'),
    url(r'^movies/(?P<title>[-\w]+)/review/$', 'apps.review.views.review'),
    
    # AJAX dynamic feed.
    url(r'^load/genre/(?P<genre>[-\w]+)/(?P<page>\d+)/$', 'apps.movie.views.load_movies'),
    url(r'^load/(?P<review_type>\w+)/(?P<title>[-\w]+)/(?P<page>\d+)/$', 'apps.movie.views.load_reviews'), 
    url(r'^load/(\w+)/(\d+)/$', 'apps.general_utilities.views.load_feed'),

    # Search. 
    url('^search/', include('haystack.urls')),
    
    # Social authentication.
    url(r'', include('social_auth.urls')),

	# Admin panel and documentation.
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),

    # Media for development.
	# django-sentry log viewer.
	#url(r'^sentry/', include('sentry.urls')),
)
