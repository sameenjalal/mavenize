from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
import api

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
    return HttpResponse(api.get_user_activity([user_id], page),
        mimetype="application/json")

@login_required
def bookmarks(request, user_id, page):
    """
    Returns the list of most recent bookmarks by a user.
    """
    pass 
