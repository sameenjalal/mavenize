from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.utils.html import escape
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core import serializers

from movie.models import Movie, Genre, Actor, Director
from review.models import Agree, ReviewForm
from social_graph.models import Forward
import api
from utils import pop_empty_keys

from sorl.thumbnail import get_thumbnail

@login_required
def explore(request, time_period=None, page=None):
    """
    If the request is not AJAX, returns the skeleton HTML.  If the
    request is AJAX, returns a list of filtered movies
    """
    if not request.is_ajax():
        return render_to_response('movie_explore.html', {},
            context_instance=RequestContext(request))

    params = {
        'genre__url__in': request.GET.getlist('genres'),
        'actors__name__in': request.GET.getlist('actors'),
        'directors__name__in': request.GET.getlist('directors'),
    }
    cleaned_params = pop_empty_keys(params)
    response = api.get_movie_thumbnails(time_period, page, cleaned_params)

    return HttpResponse(response, mimetype="application/json")


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
        try:
            sp = transaction.savepoint()
            friend_agrees = Agree.objects.select_related(
                'review','review__user').filter(giver__in=friends) \
                                        .exclude(review__user=me) \
                                        .exclude(giver=me) \
                                        .order_by('review') \
                                        .distinct('review')
            transaction.savepoint_commit(sp)
        except IntegrityError:
            transaction.savepoint_rollback(sp)
            friend_agrees = []

        context = {
            'movie': movie,
            'actors': movie.actors.all(),
            'directors': movie.directors.all(),
            'genre': movie.genre.all(),
            'friend_bookmarks': movie.item.bookmark_set.select_related(
                    'user', 'user__userprofile').filter(
                        user__in=friends),
            'my_reviews': reviews.filter(
                Q(user=me) | Q(agree__giver=me) | Q(thank__giver=me)),
            'friend_reviews': reviews.filter(user__in=friends) \
                                     .exclude(user=me) \
                                     .exclude(agree__giver=me) \
                                     .exclude(thank__giver=me),
            'friend_agrees': friend_agrees, 
            'global_reviews': reviews.exclude(
                    user__in=global_exclude
                ).exclude(agree__giver__in=global_exclude),
            'form': ReviewForm(),
            'links': movie.item.link_set.all(),
            'has_reviewed': reviews.filter(user=me).count()
        }
    except:
        raise Http404
    return render_to_response('movie_profile.html', context,
        context_instance=RequestContext(request))

@login_required
def genres(request):
    """
    Returns the list of all existing genres in JSON.
    """
    if not request.is_ajax():
        raise Http404

    response = serializers.serialize("json",
        Genre.objects.all().order_by('name') ,fields=('name', 'url'))
    return HttpResponse(response, mimetype="application/json")

@login_required
def cast(request):
    """
    Returns the list of all existing actors and directors in JSON.
    """
    if not request.is_ajax():
        raise Http404

    response = {
        'actors': list(Actor.objects.all().values_list(
            'name', flat=True)),
        'directors': list(Director.objects.all().values_list(
            'name', flat=True))
    }
    return HttpResponse(simplejson.dumps(response),
        mimetype="application/json")
