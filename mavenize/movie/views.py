from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404
from django.template import RequestContext

from mavenize.movie.models import Movie
from mavenize.movie.models import Genre
from mavenize.review.models import Review
from mavenize.review.models import ReviewForm
from django.db.models import Avg

from django.contrib.auth.decorators import login_required
# from actstream import action

@login_required
def genre(request, genre):
    genre = Genre.objects.get(name__icontains=genre)
    movies = Movie.objects.filter(genre=genre)
    movie_reviews = {}
    for movie in movies:
        try:
            movie_reviews[movie] = Review.objects.filter(
                table_number=1,
                table_id_in_table=movie.movie_id)[0]
        except:
            movie_reviews[movie] = None 
    return render_to_response('genre.html', {
            'genre': genre.name,
            'movie_reviews': movie_reviews,
        },
        context_instance=RequestContext(request))

@login_required
def profile(request, title):
    movie = get_object_or_404(Movie, url=title)
    reviews = Review.objects.filter(table_number=1, table_id_in_table=movie.movie_id)
    rating = 0
    if reviews:
        rating = int(reviews.aggregate(Avg('rating'))['rating__avg']*50)

    return render_to_response('movie_profile.html', {
        'movie': movie,
        'rating': rating,
        'reviews': reviews,
        'form': ReviewForm(),
        },
        context_instance=RequestContext(request))

