from django.contrib import admin
from apps.social_graph import models

admin.site.register(models.Following)
admin.site.register(models.Follower)

