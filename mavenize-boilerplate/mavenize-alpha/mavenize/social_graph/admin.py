from django.contrib import admin
from mavenize.social_graph import models

admin.site.register(models.Following)
admin.site.register(models.Follower)

