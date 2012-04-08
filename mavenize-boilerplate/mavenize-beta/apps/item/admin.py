from django.contrib import admin
from item.models import Item
from item.models import Link
from item.models import Popularity

admin.site.register(Item)
admin.site.register(Link)
admin.site.register(Popularity)
