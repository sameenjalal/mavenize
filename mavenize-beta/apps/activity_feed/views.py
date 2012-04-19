from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from activity_feed.models import Activity
from social_graph.models import Forward

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
    context = {
        'activities': Activity.objects.select_related(
                'sender', 'sender__userprofile').prefetch_related(
                        'target_object',
                        'target_object__user',
                        'target_object__item',
                ).filter(sender__in=friends)
    }
    return render_to_response('activity_feed.html', context,
        context_instance=RequestContext(request))
