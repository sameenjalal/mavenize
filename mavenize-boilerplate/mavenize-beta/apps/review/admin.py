from django.contrib import admin
from review.models import Review
from review.models import Agree
from review.models import Thank

admin.site.register(Review)
admin.site.register(Agree)
admin.site.register(Thank)

