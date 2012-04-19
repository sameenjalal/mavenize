from django.db import models
from django.contrib.auth.models import User

class KarmaAction(models.Model):
    recipient = models.ForeignKey(User, related_name='karma_received')
    giver = models.ForeignKey(User, related_name='karma_given')
    karma = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Karma Actions"

    def __unicode__(self):
        return "User #%s gave User #%s %s karma" % (self.giver.id,
            self.recipient.id, self.karma)
