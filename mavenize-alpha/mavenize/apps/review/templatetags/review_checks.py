from django import template
from apps.review.models import Thanks

register = template.Library()

@register.filter(name='has_reviewed')
def has_reviewed(user, movie):
    return user.review_set.filter(table_id_in_table=movie).count()
