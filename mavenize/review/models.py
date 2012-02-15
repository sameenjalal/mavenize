from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    table_number = models.IntegerField()
    table_id_in_table = models.IntegerField()
    text = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
    up_votes = models.IntegerField()
    down_votes = models.IntegerField()

    RATING_CHOICES = [(i,i) for i in range(0,3)]
    rating = models.SmallIntegerField(choices=RATING_CHOICES)

    def __unicode__(self):
        return "User #%s reviewing Movie #%s" %(self.user.id, self.table_id_in_table)

    class Meta:
        ordering = ('-created_at',)

class ReviewForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'id': 'review-text'}))
    class Meta:
        model = Review

class Thanks(models.Model):
    giver = models.IntegerField()
    review = models.ForeignKey(Review)

    def __unicode__(self):
        return "User #%s thanked Review #%s" % (self.giver, self.review.pk)
