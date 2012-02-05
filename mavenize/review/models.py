from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    table_number = models.IntegerField()
    table_id_in_table = models.IntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

	RATING_CHOICES = [(i,i) for i in range(1,6)]
	rating = models.SmallIntegerField(choices=RATING_CHOICES)
