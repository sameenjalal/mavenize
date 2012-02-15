from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as social_logout

from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from mavenize.movie.models import Movie
from mavenize.review.models import Review
from mavenize.movie.models import MoviePopularity

from mavenize.social_graph.models import Following
from mavenize.social_graph.models import Follower
# from actstream.actions import follow

from collections import OrderedDict

def index(request):
    if request.session.get('social_auth_last_login_backend') == 'facebook':
        return feed(request)
    return render_to_response('index.html', {},
        context_instance=RequestContext(request))

@login_required
def login(request):
    return redirect('/')

@login_required
def logout(request):
    social_logout(request)
    return redirect('/')

@login_required
def feed(request):
    user_id = request.user.id

    # Get the 10 most recent friend reviews
    following = Following.objects.filter(
        fb_user=user_id).values_list('follow',flat=True)
    reviews = Review.objects.filter(user__in=following)[:10]
    movies = Movie.objects.filter(
        pk__in=reviews.values_list('table_id_in_table',flat=True)).values(
            'movie_id', 'title', 'image', 'url')
    id_movies = dict([(m['movie_id'], m) for m in movies])
    ordered_movies = [id_movies[i] for i in reviews.values_list(
        'table_id_in_table', flat=True)]
    friend_reviews = OrderedDict(zip(reviews,ordered_movies))
    
    # Get the 10 most recent global reviews
    reviews = Review.objects.exclude(user__in=following).exclude(user=user_id)
    movies = Movie.objects.filter(
        pk__in=reviews.values_list('table_id_in_table',flat=True)).values(
            'movie_id', 'title', 'image', 'url')
    id_movies = dict([(m['movie_id'], m) for m in movies])
    ordered_movies = [id_movies[i] for i in reviews.values_list(
        'table_id_in_table', flat=True)]
    global_reviews = OrderedDict(zip(reviews,ordered_movies))

    # Get the top 10 most popular movies
    popular_movie_ids = MoviePopularity.objects.all().values_list(
        'movie',flat=True)[:10]
    popular_movies = Movie.objects.filter(pk__in=popular_movie_ids).values_list(
        'image',flat=True)
    return render_to_response('feed.html', {
        'popular_movies': popular_movies,
        'friend_reviews': friend_reviews,
        'global_reviews': global_reviews
        },
        context_instance=RequestContext(request))

