from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from mavenize.movie.models import Movie
from mavenize.review.models import Review

from mavenize.social_graph.models import Following
from mavenize.social_graph.models import Follower
from actstream.actions import follow

from social_auth.signals import socialauth_registered

import facebook
import requests
import sys

def index(request):
    if request.user:
        return feed(request)

    return render_to_response('index.html', {},
        context_instance=RequestContext(request))

@login_required
def login(request):
	return redirect('/')

@login_required
def feed(request):
	reviews = Review.objects.all()[:20]
	global_reviews = {}
	friend_reviews = {}

	for review in reviews:
		global_reviews[review] = Movie.objects.get(movie_id=review.table_id_in_table)

	return render_to_response('feed.html', {
		'friend_reviews': friend_reviews,
		'global_reviews': global_reviews
		},
		context_instance=RequestContext(request))

# Create following relationships the first time a user signs up
def new_user_handler(sender, user, response, details, **kwargs):
	social_user = user.social_auth.get(provider='facebook')
	graph = facebook.GraphAPI(social_user.extra_data['access_token'])
	friends = graph.get_connections("me", "friends")['data']
	friend_ids = []
	
	for friend in friends:
		friend_ids.append(friend['id'])
	
	signed_up = UserSocialAuth.objects.filter(uid__in=friend_ids)
	for friend in signed_up:
		follow(user, friend.user)
		follow(friend.user, user)

socialauth_registered.connect(new_user_handler, sender=None)
