from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from movie.models import Movie
from review.models import Agree, ReviewForm
from social_graph.models import Forward

from sorl.thumbnail import get_thumbnail

@login_required
def explore(request, time_period=None, page=None):
    if not request.is_ajax():
        return render_to_response('movie_explore.html', {},
            context_instance=RequestContext(request))

    movies = Movie.objects.all() \
            .order_by('-item__popularity__' + time_period) \
            .values('title', 'url', 'synopsis', 'image', 'theater_date')
    paginator = Paginator(movies, 20)

    try:
        next_page = paginator.page(page).next_page_number()
        paginator.page(next_page)
    except (EmptyPage, InvalidPage):
        next_page = ''

    response = [{ 
        'title': movie['title'],
        'url': reverse('movie-profile', args=[movie['url']]),
        'synopsis': movie['synopsis'][:140],
        'image_url': get_thumbnail(movie['image'], 'x285').url,
        'next': next_page 
    } for movie in paginator.page(page)] 

    return HttpResponse(simplejson.dumps(response),
        mimetype="application/json")

@ensure_csrf_cookie
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
