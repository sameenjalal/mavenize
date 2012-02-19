from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import Http404
from django.template import RequestContext

from django.contrib.auth.models import User
from mavenize.movie.models import Movie
from mavenize.movie.models import Genre
from mavenize.review.models import Review
from mavenize.review.models import ReviewForm
from mavenize.social_graph.models import Following
from django.db.models import Avg
from mavenize.general_utilities.utils import aggregate_reviews

from django.contrib.auth.decorators import login_required
# from actstream import action

@login_required
def genre(request, genre):
    context = load_movies(request, genre, 1)

    return render_to_response(
        'genre.html',
        context,
        context_instance=RequestContext(request)
    )

@login_required
def profile(request, title):
    context = load_reviews(request, title, None, 1)
    context['rating'] = 0
    context['form'] = ReviewForm()

    reviews = Review.objects.filter(
        table_id_in_table=context['movie'].movie_id)
    context['votes'] = reviews.count()    
    ratings = reviews.aggregate(Avg('rating'))['rating__avg']
    if ratings:
        context['rating'] = ratings * 50
    
    return render_to_response('movie_profile.html', 
        context,
        context_instance=RequestContext(request)
    )

def load_reviews(request, title, review_type, page):
    context = {}
    
    following = Following.objects.filter(
        fb_user=request.user.id).values_list('follow', flat=True)
    context['movie'] = get_object_or_404(Movie, url=title)
    context['friend_reviews'] = aggregate_reviews(
        request.user.id,
        Review.objects.filter(
            table_id_in_table=context['movie'].movie_id
        ).filter(user__in=following).order_by('-up_votes').values(
                'review_id',
                'user',
                'text',
                'up_votes',
                'created_at'
            )[10*(int(page)-1):10*int(page)]
    )
    review_count = len(context['friend_reviews'])

    if request.is_ajax() and review_type == 'friend':
        if not review_count:
            return HttpResponse(status=204)

        return render_to_response(
            'partials/movie_friend_review.html',
            context,
            context_instance=RequestContext(request)
        )

    if review_count < 10:
        context['global_reviews'] = aggregate_reviews(
            request.user.id,
            Review.objects.filter(
                table_id_in_table=context['movie'].movie_id
            ).exclude(user__in=following).order_by('-up_votes').values(
                    'review_id',
                    'user',
                    'text',
                    'up_votes',
                    'created_at'
                )[10*(int(page)-1):10*int(page)]
        )

        if request.is_ajax() and review_type == 'global':
            if not context['global_reviews']:
                return HttpResponse(status=204)

            return render_to_response(
                'partials/movie_global_review.html',
                context,
                context_instance=RequestContext(request)
            )

    return context

def load_movies(request, genre, page):
    context = {}

    context['genre'] = get_object_or_404(Genre, url=genre)
    movies = Movie.objects.filter(
        genre=context['genre'])[10*(int(page)-1):10*int(page)]
    movie_reviews = {}
    for movie in movies:
        try:
            review = Review.objects.filter(
                table_id_in_table=movie.movie_id
            ).values('review_id', 'user', 'text', 'up_votes', 'created_at')[0]
            review['first_name'] = User.objects.get(id=review['user']).first_name
            movie_reviews[movie] = review
        except:
            movie_reviews[movie] = None 
    
    context['movie_reviews'] = movie_reviews
    
    if request.is_ajax():
        return render_to_response(
            'partials/movie_results.html',
            context,
            context_instance=RequestContext(request)
        )

    return context
