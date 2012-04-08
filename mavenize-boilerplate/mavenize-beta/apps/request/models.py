from django.db import models
from django.contrib.auth.models import User

from item.models import Item

class Request(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    responses = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s requesting Item #:%s" % (self.user.get_full_name(),
            self.item.id)
