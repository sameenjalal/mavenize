from django.shortcuts import render_to_response
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from movie.models import Movie
from social_graph.models import Forward
@login_required
def profile(request, title):
    try:
        movie = Movie.objects.select_related(
            'item').prefetch_related('actors', 'directors', 'genre').get(
                url=title)
        me = request.user.id
        friends = list(Forward.objects.filter(
            source_id=me).values_list('destination_id', flat=True))
        global_exclude = friends + [me]
        reviews = movie.item.review_set.select_related(
            'user', 'user__userprofile').all()
        context = {
            'movie': movie,
            'actors': movie.actors.all(),
            'directors': movie.directors.all(),
            'genre': movie.genre.all(),
            'friend_bookmarks': movie.item.bookmark_set.select_related(
                    'user', 'user__userprofile').filter(
                        user__in=friends),
            'my_reviews': reviews.filter(
                    Q(user=me) | Q(agree__giver=me)),
            'friend_reviews': reviews.filter(
                    Q(user__in=friends) |
                    Q(agree__giver__in=friends)
                ).exclude(user=me).exclude(agree__giver=me),
            'global_reviews': reviews.exclude(
                    user__in=global_exclude
                ).exclude(agree__giver__in=global_exclude),
            'links': movie.item.link_set.all(),
        }
    except:
        raise Http404
    return render_to_response('movie_profile.html', context,
        context_instance=RequestContext(request))
