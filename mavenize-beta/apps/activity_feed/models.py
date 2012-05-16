from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

class Activity(models.Model):
    sender = models.ForeignKey(User)
    verb = models.CharField(max_length=30)
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    target_object = generic.GenericForeignKey('content_type',
        'object_id')
    created_at = models.DateTimeField(auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Activities"

    def __unicode__(self):
        return "User #%s %s Review #%s" % (self.sender.id, 
            self.verb, self.object_id)
