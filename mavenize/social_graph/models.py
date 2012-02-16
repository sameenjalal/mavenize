from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete

class Following(models.Model):
    id = models.AutoField(primary_key=True)
    fb_user = models.BigIntegerField(default=0)
    follow = models.BigIntegerField(default=0)

    def __unicode__(self):
        return "User #%s following User #%s" %(self.fb_user, self.follow)

class Follower(models.Model):
    id = models.AutoField(primary_key=True)
    fb_user = models.BigIntegerField(default=0)
    follow = models.BigIntegerField(default=0)

    def __unicode__(self):
        return "User #%s following User #%s" %(self.fb_user, self.follow)

def delete_relationships(sender, instance, **kwargs):
    Following.objects.filter(fb_user=instance.id).delete()
    Following.objects.filter(follow=instance.id).delete()
    Follower.objects.filter(fb_user=instance.id).delete()
    Follower.objects.filter(follow=instance.id).delete()

post_delete.connect(delete_relationships, sender=User)
