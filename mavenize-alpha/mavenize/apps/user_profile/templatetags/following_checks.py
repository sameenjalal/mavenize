from django import template
from apps.social_graph.models import Following

register = template.Library()

@register.filter(name="is_following")
def is_following(user, following):
    return Following.objects.filter(fb_user=user, follow=following).count() \
        or user == following
