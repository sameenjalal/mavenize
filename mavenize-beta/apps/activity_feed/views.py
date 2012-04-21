from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.db.models import Sum
from django.contrib.auth.models import User

from activity_feed.models import Activity
from leaderboard.models import KarmaAction
from social_graph.models import Forward

import datetime as dt

def index(request):
    if request.user.is_authenticated():
        return activity_feed(request)
    else:
        return render_to_response('index.html', {},
            context_instance=RequestContext(request))

def activity_feed(request):
    me = request.user.id
    friends = Forward.objects.filter(
        source_id=me).values_list('destination_id', flat=True)
    us = list(friends)+ [me]
    last_seven_days = dt.datetime.now() - dt.timedelta(days=7)
    beneficiary_rankings = (
        KarmaAction.objects.filter(created_at__gte=last_seven_days) \
                           .filter(recipient=me) \
                           .exclude(giver=me) \
                           .values('giver') \
                           .annotate(total_given=Sum('karma')) \
                           .order_by('-total_given')[:5])
    leaderboard_rankings = (
        KarmaAction.objects.filter(created_at__gte=last_seven_days) \
                           .filter(giver__in=us) \
                           .values('giver') \
                           .annotate(total_given=Sum('karma')) \
                           .order_by('-total_given'))
    try:
        my_ranking = [i for i, v in enumerate(leaderboard_rankings)
            if v['giver'] == me][0]
    except IndexError:
        my_ranking = 0
    my_relative_leaderboard, start_index = compute_relative_leaderboard(
        my_ranking,
        match_users_with_karma(leaderboard_rankings)
    )
    context = {
        'activities': Activity.objects.select_related(
                            'sender',
                            'sender__userprofile').prefetch_related(
                                    'target_object',
                                    'target_object__user',
                                    'target_object__item',
                                    'target_object__item__movie'
                            ).filter(sender__in=friends)[:20],
        'leaderboard': my_relative_leaderboard,
        'start_index': start_index,
        'beneficiaries': match_users_with_karma(beneficiary_rankings) 
    }
    return render_to_response('activity_feed.html', context,
        context_instance=RequestContext(request))

def match_users_with_karma(rankings):
    """
    Create a dictionary that maps user objects to karma given.
    """
    giver_ids = [r['giver'] for r in rankings]
    ids_to_users = User.objects.select_related('userprofile').in_bulk(
        giver_ids)
    return [(ids_to_users[r['giver']], r['total_given']) \
        for r in rankings]

def compute_relative_leaderboard(ranking, leaderboard_rankings):
    size = len(leaderboard_rankings) 
    if ranking == 0 or ranking == 1:
        return (leaderboard_rankings[:5], 0)
    elif ranking == size or ranking == size-1:
        return (leaderboard_rankings[-5:], max(0,size-5))
    else:
        return (leaderboard_rankings[ranking-2:ranking+3],
            max(0, size-2))
