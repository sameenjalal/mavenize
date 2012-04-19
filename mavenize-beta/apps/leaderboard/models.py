from django.db import models
from django.contrib.auth.models import User

class KarmaActions(models.Model):
    user = models.ForeignKey(User)
    sender = models.ForeignKey(User)
    karma = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "User #%s gave %s %s karma" % (self.sender_id,
            self.user.id, self.created_at)
