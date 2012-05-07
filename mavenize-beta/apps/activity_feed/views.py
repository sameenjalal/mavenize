from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import api

import datetime as dt

def index(request):
    if request.user.is_authenticated():
        return activity_feed(request)
    else:
        return render_to_response('index.html', {},
            context_instance=RequestContext(request))

@login_required
def activity_feed(request):
    """
    Renders the activity feed home page for an authenticated user.
    """
    me = request.session['_auth_user_id']
    last_seven_days = dt.datetime.now() - dt.timedelta(days=7)
    relative_leaderboard, start_index = api.get_relative_leaderboard(
        me, last_seven_days)
    context = {
        'leaderboard': relative_leaderboard,
        'start_index': start_index,
        'beneficiaries': api.get_beneficiary_leaderboard(
            me, last_seven_days) 
    }
    return render_to_response('activity_feed.html', context,
        context_instance=RequestContext(request))

@login_required
def activity(request, page):
    """
    Returns the list of most recent activities by the users that the
    current user follows.
    """
    me = request.session['_auth_user_id']
    following = api.get_following(me)
    return HttpResponse(api.get_user_activity(following, page),
        mimetype="application/json")
