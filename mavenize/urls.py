from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.views.static import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', direct_to_template, {'template': 'index.html'}, name='index'),
	url(r'^logged-in/$', 'mavenize.views.login'),
	url(r'^feed/$', direct_to_template, {'template': 'feed.html'}),
	url(r'^users/dqai$', direct_to_template, {'template': 'friend_profile.html'}),
	url(r'^search/$', direct_to_template, {'template': 'search.html'}),
	url(r'^category/action/$', direct_to_template, {'template': 'category.html'}),

	url(r'^movies/(?P<title>[-\w]+)/$', 'mavenize.movie.views.profile'),
	url(r'^activity/', include('actstream.urls')),
	url(r'', include('social_auth.urls')),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': settings.MEDIA_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

     url(r'^admin/', include(admin.site.urls)),
)
