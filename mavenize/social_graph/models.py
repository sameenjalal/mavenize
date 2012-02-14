from django.db import models

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
