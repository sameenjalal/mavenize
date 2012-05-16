from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Notification(models.Model):
    sender_id = models.BigIntegerField(default=0)
    recipient_id = models.BigIntegerField(default=0)
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    notice_object = generic.GenericForeignKey('content_type',
        'object_id')
    created_at = models.DateTimeField(auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __unicode__(self):
        return "User %s sending notifcation to User %s" % \
            (self.sender_id, self.recipient_id)
