from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from movie.models import Movie
from social_graph.models import Forward

@login_required
def profile(request, title):
    try:
        movie = Movie.objects.select_related(
            'item').prefetch_related('actors', 'directors').get(url=title)
        friends = list(Forward.objects.filter(
            source_id=request.user.id).values_list(
                'destination_id', flat=True))
        context = {
            'movie': movie,
            'actors': movie.actors.all(),
            'directors': movie.directors.all(),
            'bookmarked': movie.item.bookmark_set.filter(
                user__in=friends).values_list('user', flat=True),
            'my_reviews': movie.item.review_set.select_related(
                'user').filter(user=request.user.id,
                               agree__giver=request.user.id),
            'friend_reviews': movie.item.review_set.select_related(
                'user').filter(user__in=friends,
                               agree__giver__in=friends),
            'global_reviews': movie.item.review_set.select_related(
                'user').exclude(user__in=friends,
                                agree__giver__in=friends)[:10],
            'links': movie.item.link_set.all(),
            'rating': movie.item.get_rating(),
            'votes': movie.item.get_votes()
        }
    except:
        raise Http404
    return render_to_response('movie_profile.html', context,
        context_instance=RequestContext(request))
