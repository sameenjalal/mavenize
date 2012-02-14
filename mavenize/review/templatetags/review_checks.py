from django import template
from mavenize.review.models import Thanks

register = template.Library()

@register.filter(name='has_thanked')
def has_thanked(user, review):
    return Thanks.objects.filter(
        giver=user,review=review).count() or user == review.user.id

@register.filter(name='has_reviewed')
def has_reviewed(user, movie):
    return user.review_set.filter(table_id_in_table=movie).count()
