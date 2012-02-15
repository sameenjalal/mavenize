from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404
from django.template import RequestContext

from django.contrib.auth.models import User
from mavenize.movie.models import Movie
from mavenize.movie.models import Genre
from mavenize.review.models import Review
from mavenize.review.models import ReviewForm
from mavenize.review.models import Thanks
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
    rating = int(reviews.aggregate(Avg('rating'))['rating__avg']*50)
    user = request.user
    form = ReviewForm()

    return render_to_response('movie_profile.html', {
        'movie': movie,
        'rating': rating,
        'reviews': reviews,
        'form': form,
        },
        context_instance=RequestContext(request))

@login_required
def review(request, title):
    if request.method == 'POST':
        movie = Movie.objects.get(url=title)
        review = {
            'user': request.session['_auth_user_id'],
            'table_number': 1,
            'table_id_in_table': movie.movie_id,
            'text': request.POST['text'],
            'up_votes': 0,
            'down_votes': 0,
        }
        # Convert rating to numerical value for review
        if request.POST['submit'] == "Loved It":
            review['rating'] = 2
        elif request.POST['submit'] == "So-So":
            review['rating'] = 1
        else:
            review['rating'] = 0
        form = ReviewForm(review)
        if form.is_valid():
            form.save()
            movie.moviepopularity.popularity += review['rating']
            movie.moviepopularity.save()
            # action.send(request.user, verb="raved about", action_object=form, target=movie)

    return redirect(request.META.get('HTTP_REFERER', None))

