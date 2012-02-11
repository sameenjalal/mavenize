from django.db import models

class Following(models.Model):
    id = models.AutoField(primary_key=True)
    fb_user = models.IntegerField(default=0)
    follow = models.IntegerField(default=0)

class Follower(models.Model):
    id = models.AutoField(primary_key=True)
    fb_user = models.IntegerField(default=0)
    follow = models.IntegerField(default=0)
