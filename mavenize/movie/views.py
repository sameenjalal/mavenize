from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from mavenize.movie.models import Movie

from django.contrib.auth.decorators import login_required

@login_required
def review(request, name):
	try:
		review = Review.objects.create(
			user = User.objects.get(id=request.session['_auth_user_id']),
			table_number=1,
			table_id_in_table=Movie.objects.get(id=)
		)
