from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.utils import simplejson
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.utils.timesince import timesince

from django.contrib.auth.models import User
from activity_feed.models import Activity

from sorl.thumbnail import get_thumbnail

@login_required
def profile(request, user_id):
    try:
        context = {
            'user': User.objects.select_related('userprofile',
                'userstatistics').get(pk=user_id)
        }
    except:
        raise Http404 

    return render_to_response("user_profile.html", context,
        RequestContext(request))

@login_required
def activity(request, user_id, page):
    """
    Returns the list of most recent activities by a user.
    """
    activities = Activity.objects.select_related('sender',
                                                 'sender__userprofile') \
                    .prefetch_related('target_object',
                                      'target_object__user',
                                      'target_object__item',
                                      'target_object__item__movie') \
                    .filter(sender=user_id)

    paginator = Paginator(activities, 20)
    
    try:
        next_page = paginator.page(page).next_page_number()
        paginator.page(next_page)
    except (EmptyPage, InvalidPage):
        next_page = ''

    response = [{
        'object_id': activity.object_id,
        'sender_avatar': get_thumbnail(
            activity.sender.userprofile.avatar, '100x100', crop='center').url,
        'rating': activity.target_object.rating,
        'target_url': reverse('movie-profile',
            args=[activity.target_object.item.movie.url]),
        'target_image': get_thumbnail(
            activity.target_object.item.movie.image, 'x295').url,
        'target_title': activity.target_object.item.movie.title,
        'sender_id': activity.sender_id,
        'sender_url': reverse('user-profile', args=[activity.sender_id]),
        'sender_full_name': activity.sender.get_full_name(),
        'verb': activity.verb,
        'target_user_id': activity.target_object.user_id,
        'target_user_url': reverse('user-profile',
            args=[activity.target_object.user_id]),
        'target_user_full_name': activity.target_object.user \
                                         .get_full_name(),
        'target_user_first_name': activity.target_object.user \
                                          .first_name.lower(),
        'text': escape(activity.target_object.text),
        'time_since': timesince(activity.created_at),
    } for activity in activities]
    return HttpResponse(simplejson.dumps(response),
        mimetype="application/json")

@login_required
def bookmarks(request, user_id, page):
    """
    Returns the list of most recent bookmarks by a user.
    """
    pass 
