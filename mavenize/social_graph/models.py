from django.db import models

class Following(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField()
    follow = models.IntegerField()

class Follower(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField()
    follow = models.IntegerField()
