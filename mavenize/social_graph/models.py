from django.db import models
from django.contrib.auth.models import User

class Following(models.Model):
	user = models.ForeignKey(User)
	following = models.IntegerField()

class Follower(models.Model):
	user = models.ForeignKey(User)
	follower = models.IntegerField()
