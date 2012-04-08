from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.http import Http404

from django.contrib.auth.models import User
from mavenize.movie.models import Movie
from mavenize.review.models import Review
from mavenize.social_graph.models import Following
from mavenize.social_graph.models import Follower

from django.contrib.auth.decorators import login_required

def follow(request, id):
    if request.is_ajax():
        user_id = request.user.id
        Following.objects.get_or_create(fb_user=user_id, follow=id)
        Follower.objects.get_or_create(fb_user=id, follow=user_id)
        
        return redirect(request.META.get('HTTP_REFERER', None))
    
    else:
        raise Http404
