from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as social_logout
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify

from mavenize.user_profile.models import UserProfile
from mavenize.movie.models import Movie
from mavenize.review.models import Review
from mavenize.review.models import Thanks
from mavenize.movie.models import MoviePopularity
from mavenize.social_graph.models import Following
# from actstream.actions import follow

from mavenize.general_utilities.utils import retrieve_objects
from urllib2 import urlopen, HTTPError
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
    context = load_feed(request, None, 1) 

    # Get the top 8 most popular movies
    pm_id = MoviePopularity.objects.all().values_list('movie',flat=True)[:4]
    context['popular_movies'] = Movie.objects.filter(pk__in=pm_id).values(
        'image', 'url')

    return render_to_response('feed.html', context,
        context_instance=RequestContext(request))
        
def load_feed(request, review_type, page):
    user_id = request.user.id
    context = {}
    
    # Retrieve the 10 most recent friends reviews
    following = Following.objects.filter(
        fb_user=user_id).values_list('follow',flat=True)
    friend_reviews = Review.objects.filter(user__in=following).values(
        'review_id',
        'user',
        'table_id_in_table',
        'text',
        'up_votes',
        'created_at'
    )[10*(int(page)-1):10*int(page)]
    review_count = len(friend_reviews)

    if review_count:
        context['friend_reviews'] = aggregate(user_id, friend_reviews)

    if request.is_ajax() and review_type == 'friend':
        return render_to_response(
            'partials/friend_review.html',
            context,
            context_instance=RequestContext(request)
        )
    
    # If there are less than 10, supplement them with global reviews
    if review_count < 10:
        global_reviews = Review.objects.exclude(
            user__in=following).exclude(user=user_id).values(
            'review_id',
            'user',
            'table_id_in_table',
            'text',
            'up_votes',
            'created_at'
        )[10*(int(page)-1):(10-review_count)*int(page)]
        
        context['global_reviews'] = aggregate(user_id, global_reviews)

        if request.is_ajax() and review_type == 'global':
            return render_to_response(
                'partials/global_review.html',
                context,
                context_instance=RequestContext(request)
            )
    
    return context

# Creates a tuple of reviews and movies for a given user and set of reviews
def aggregate(user, reviews):
    uids = []
    rids = []
    mids = []
    
    for r in reviews:
        uids.append(r['user'])
        rids.append(r['review_id'])
        mids.append(r['table_id_in_table'])

    users = retrieve_objects(
        uids, 'auth', 'User', 'id', 'first_name')
    thanked_reviews = Thanks.objects.filter(review__in=rids).filter(
        giver=user).values_list('review', flat=True)

    for review, user in zip(reviews, users):
        review.update(user)
        if review['review_id'] in thanked_reviews:
            review['thanked'] = True
        else:
            review['thanked'] = False

    movies = retrieve_objects(
        mids, 'movie', 'Movie', 'movie_id', 'title', 'image', 'url')

    return zip(reviews, movies)
