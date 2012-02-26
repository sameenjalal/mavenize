from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404

from mavenize.movie.models import Movie
from mavenize.review.models import Review
from mavenize.review.models import Thanks
from mavenize.review.models import ReviewForm

from django.contrib.auth.decorators import login_required

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
            user_profile = request.user.get_profile()

            form.save()
            movie.moviepopularity.popularity += review['rating']
            movie.moviepopularity.save()
            user_profile.reviews += 1
            user_profile.save()
            # action.send(request.user, verb="raved about", action_object=form, target=movie)

    return redirect(request.META.get('HTTP_REFERER', None))

@login_required
def thank(request, review_id):
    if request.is_ajax():
        review = get_object_or_404(Review, pk=review_id)
        thank, created = Thanks.objects.get_or_create(
            giver = request.user.id,
            review = review
        )
        if created:
            receiver_profile = review.user.get_profile()
            giver_profile = request.user.get_profile()

            review.up_votes += 1
            review.save()
            receiver_profile.thanks_received += 1
            receiver_profile.save()
            giver_profile.thanks_given += 1
            giver_profile.save()

        return redirect(request.META.get('HTTP_REFERER', None))
    
    else:
        raise Http404

