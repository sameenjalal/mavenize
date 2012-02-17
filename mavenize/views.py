from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as social_logout
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify

from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from mavenize.user_profile.models import UserProfile
from mavenize.movie.models import Movie
from mavenize.review.models import Review
from mavenize.movie.models import MoviePopularity

from mavenize.social_graph.models import Following
from mavenize.social_graph.models import Follower
# from actstream.actions import follow

from collections import OrderedDict
from urllib2 import urlopen, HTTPError
from itertools import chain
import facebook

def index(request):
    if request.session.get('social_auth_last_login_backend') == 'facebook':
        return feed(request)
    return render_to_response('index.html', {},
        context_instance=RequestContext(request))

@login_required
def login(request):
    user_id = request.user.id
    social_user = request.user.social_auth.get(provider='facebook')
    graph = facebook.GraphAPI(social_user.extra_data['access_token'])

    profile, created = UserProfile.objects.get_or_create(
        user=request.user)

    if created:
        url = "http://graph.facebook.com/%s/picture" % social_user.uid 
        small_picture = urlopen(url, timeout=30)
        large_picture = urlopen(url+'?type=large', timeout=30)
        profile.picture_small.save(
            slugify(user_id)+u'.jpg',
            ContentFile(small_picture.read())
        )
        profile.picture_large.save(
            slugify(user_id)+u'_large.jpg',
            ContentFile(large_picture.read()),
        )

    return redirect('/')

@login_required
def logout(request):
    social_logout(request)
    return redirect('/')

@login_required
def feed(request):
    user_id = request.user.id
    global_reviews = {}
    gm_id = []
    
    # Get the top 8 most popular movies
    pm_id = MoviePopularity.objects.all().values_list('movie',flat=True)[:8]

    # Retrieve the 20 most recent friends reviews
    following = Following.objects.filter(
        fb_user=user_id).values_list('follow',flat=True)

    friend_reviews = Review.objects.filter(user__in=following)[:20]
    count = len(friend_reviews)
    fm_id = friend_reviews.values_list('table_id_in_table', flat=True)
    
    # If there are less than 20, supplement them with global reviews
    if count < 20:
        global_reviews = Review.objects.exclude(
            user__in=following).exclude(user=user_id)[:(20-count)]
        gm_id = global_reviews.values_list('table_id_in_table', flat=True)
    
    # Get the corresponding movie for each review
    movies = Movie.objects.filter(pk__in=list(chain(fm_id,gm_id,pm_id))).values(
        'movie_id', 'title', 'image', 'url')
    id_movies = dict([(m['movie_id'], m) for m in movies])
    popular_movies = [id_movies[i] for i in pm_id]
    friend_movies = [id_movies[i] for i in fm_id]
    global_movies = [id_movies[i] for i in gm_id]

    return render_to_response('feed.html', {
        'popular_movies': popular_movies,
        'friend_reviews': OrderedDict(zip(friend_reviews, friend_movies)),
        'global_reviews': OrderedDict(zip(global_reviews, global_movies))
        },
        context_instance=RequestContext(request))

