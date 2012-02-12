from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404
from django.template import RequestContext

from django.contrib.auth.models import User
from mavenize.movie.models import Movie
from mavenize.review.models import Review
from mavenize.review.models import ReviewForm

from django.contrib.auth.decorators import login_required
from actstream import action

@login_required
def profile(request, title):
	has_reviewed = False
	movie = get_object_or_404(Movie, url=title)
	user = request.user
	form = ReviewForm()

	if user.review_set.filter(table_id_in_table=movie.movie_id):
		has_reviewed=True
	return render_to_response('movie_profile.html', {
		'movie': movie,
		'reviews': Review.objects.filter(table_id_in_table=movie.movie_id),

		'form': form,
		'has_reviewed': has_reviewed},
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
			review['rating'] = 3
		elif request.POST['submit'] == "So-So":
			review['rating'] = 2
		else:
			review['rating'] = 1
		form = ReviewForm(review)
		if form.is_valid():
			form.save()
			action.send(request.user, verb="raved about", action_object=movie)

	return redirect(request.META.get('HTTP_REFERER', None))

