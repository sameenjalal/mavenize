from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.models import User
from mavenize.movie.models import Movie
from mavenize.review.models import Review
from mavenize.review.models import Thanks
from mavenize.social_graph.models import Following
from mavenize.social_graph.models import Follower

from django.contrib.auth.decorators import login_required

from itertools import chain

@login_required
def profile(request, id):
    target_user = User.objects.get(pk=id) 
    target_profile = target_user.get_profile()
    positive_movies = []
    neutral_movies = []
    negative_movies = []

    following = Following.objects.filter(fb_user=id).values_list(
        'follow', flat=True)[:3]
    followers = Follower.objects.filter(fb_user=id).values_list(
        'follow', flat=True)[:3]

    positive_reviews = Review.objects.filter(
        user=id, rating=2).values_list('table_id_in_table', flat=True)
    neutral_reviews = Review.objects.filter(
        user=id, rating=1).values_list('table_id_in_table', flat=True)
    negative_reviews = Review.objects.filter(
        user=id, rating=0).values_list('table_id_in_table', flat=True)
    positive_movies = Movie.objects.filter(pk__in=positive_reviews).values(
        'image', 'url')
    neutral_movies = Movie.objects.filter(pk__in=neutral_reviews).values(
        'image', 'url')
    negative_movies = Movie.objects.filter(pk__in=negative_reviews).values(
        'image', 'url')
    
    # Filter into positive, neutral, and negative reviews

    return render_to_response('user_profile.html', {
           'target_user': target_user,
           'following': following,
           'followers': followers,
           'positive_movies': positive_movies,
           'neutral_movies': neutral_movies,
           'negative_movies': negative_movies,
           'target_profile': target_profile
        },
        RequestContext(request)) 
