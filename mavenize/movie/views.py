from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404

from django.contrib.auth.models import User
from mavenize.movie.models import Movie
from mavenize.review.models import Review

from django.contrib.auth.decorators import login_required

@login_required
def profile(request, title):
	movie = get_object_or_404(Movie, url=title)
	user = User.objects.get(id=request.session['_auth_user_id'])
	if not user.review_set.filter(table_id_in_table=movie.movie_id):
		form = 1	
		#form = ReviewForm()
	return render_to_response('movie_profile.html', {
		'movie': movie,
		'reviews': Review.objects.filter(table_id_in_table=movie.movie_id),

		'form': form})

@login_required
def review(request, url):
	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			review = Review.objects.create(
				user = User.objects.get(id=request.session['_auth_user_id']),
				table_number = 1,
				table_id_in_table = Movie.objects.get(url=url).movie_id,
				text = request.POST['review'],
				up_votes = 0,
				down_votes = 0,
				rating = request.POST['rating'],
			)
			
	return redirect(request.META.get('HTTP_REFERER', None))

