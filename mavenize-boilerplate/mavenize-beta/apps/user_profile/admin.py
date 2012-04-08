from django.contrib import admin
from user_profile.models import UserProfile
from user_profile.models import UserStatistics

admin.site.register(UserProfile)
admin.site.register(UserStatistics)
