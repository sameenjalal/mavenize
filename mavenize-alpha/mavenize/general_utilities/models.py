from django.db import models
from django.forms import ModelForm
from django.forms import Textarea
from django.contrib.auth.models import User

class Feedback(models.Model):
    user = models.ForeignKey(User)
    message = models.TextField()

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        widgets = { 'message': Textarea(attrs={'id': 'review-text' })}
