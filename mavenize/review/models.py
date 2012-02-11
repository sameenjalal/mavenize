from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
	review_id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User)
	table_number = models.IntegerField()
	table_id_in_table = models.IntegerField()
	text = models.CharField(max_length=240)
	created_at = models.DateTimeField(auto_now=True)
	up_votes = models.IntegerField()
	down_votes = models.IntegerField()

	RATING_CHOICES = [(i,i) for i in range(1,4)]
	rating = models.SmallIntegerField(choices=RATING_CHOICES)
