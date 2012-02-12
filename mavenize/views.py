from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth

from mavenize.social_graph.models import Following
from mavenize.social_graph.models import Follower

import facebook
import requests
import sys

def index(request):
    #if request.session.get('_auth_user_id'):
        #try:
            #friends = Profile.objects.get(
                #user=request.session['_auth_user_id']).friends.keys()
            #return feed(request, friends)
        #except:
            #pass

    return render_to_response('index.html', {},
        context_instance=RequestContext(request))

@login_required
def login(request):
    # TODO: IF the user logs in for the first time, do
    if request.session.get('_auth_user_id'):
        try:
            user = request.session['_auth_user_id']
            social = UserSocialAuth.objects.get(user=user)

            graph = facebook.GraphAPI(social.extra_data['access_token'])

            my_id = graph.get_object("me")['id']
            connections = graph.get_connections("me", "friends")['data']
            my_conn_list = []

            i = 1
            for friend in connections:
                # TODO: Only if friend is already in user db add
                print i
                i = i + 1
                try:
                    fg = Following.objects.create(fb_user=my_id,follow=friend['id'])
                    fr = Follower.objects.create(fb_user=friend['id'],follow=my_id)

                    fg.save()
                    fr.save()
                except:
                    pass
        except:
            print "Unexpected error nigga:", sys.exc_info()[0]
            raise

    return redirect('/')

@login_required
def feed(request, friends):
    context = {}
    friends_most_recent = {}
    user_reviews = {}

    #for friend in friends:
        #try:
            #review = UserSocialAuth.objects.get(uid=friend).user.productreview_set.all().order_by('-timestamp')[0]
            #if review:
                #friends_most_recent[friend] = review.timestamp
        #except:
            #pass
    #if len(friends_most_recent) < 1:
        #messages.add_message(request, messages.INFO, 'No Reviews Found')
    #else:
        #sorted_by_time = OrderedDict(sorted(friends_most_recent.items(),
            #key=lambda x: x[1]))
        #for friend, timestamp in sorted_by_time.items():
            #user = UserSocialAuth.objects.get(uid=friend).user
            #user_reviews[user] = ProductReview.objects.get(
                #user=user.id, timestamp=timestamp)

    context['name'] = User.objects.get(
        id=request.session['_auth_user_id']).first_name
    context['reviews'] = user_reviews

    return render_to_response('feed.html', context,
        context_instance=RequestContext(request))
