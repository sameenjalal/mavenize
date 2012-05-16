from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

import api

@login_required
def follow(request, user_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            api.follow(request.session['_auth_user_id'], user_id)
            return HttpResponse(status=201)
        except:
            return HttpResponse(status=500)
    
    raise Http404

@login_required
def unfollow(request, user_id):
    if request.method == 'DELETE' and request.is_ajax():
        try:
            api.unfollow(request.session['_auth_user_id'], user_id)
            return HttpResponse(status=201)
        except:
            return HttpResponse(status=500)

    raise Http404
    
