from django.contrib import admin
from social_graph.models import Forward
from social_graph.models import Backward

admin.site.register(Forward)
admin.site.register(Backward)
