from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from django import forms

from item.models import Item
from activity_feed.models import Activity
from leaderboard.models import KarmaAction
from notification.models import Notification
from user_profile.models import UserStatistics

import datetime as dt

class Review(models.Model):
    RATING_CHOICES = [(i,i) for i in range(1,5)] 

    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    text = models.TextField()
    rating = models.SmallIntegerField(choices=RATING_CHOICES)
    agrees = models.IntegerField(default=0)
    thanks = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
     
    def __unicode__(self):
        return "%s reviewing Item #%s" % (self.user.get_full_name(),
            self.item.id)

class ReviewForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
            'id': 'review-text',
            'placeholder': 'Tell us what you thought, choose a rating, and rave!',
            'rows': 1,
        }))

    class Meta:
        model = Review

class Agree(models.Model):
    giver = models.ForeignKey(User)
    review = models.ForeignKey(Review)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s agreeing with Review #%s" % \
            (self.giver.get_full_name(), self.review.id)

class Thank(models.Model):
    giver = models.ForeignKey(User)
    review = models.ForeignKey(Review)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s thanking Review #%s" % \
            (self.giver.get_full_name(), self.review.id)

@receiver(post_save, sender=Review)
def create_review(sender, instance, created, **kwargs):
    """
    Create an activity for the review.
    Create a karma action for the review.
    Increment the user's reviews by one and karma by five.
    Increment the item's ratings by the review's rating.
    """
    if created:
        Activity.objects.create(
            sender=instance.user,
            verb="raved about",
            target_object=instance
        )
        KarmaAction.objects.create(
            recipient=instance.user,
            giver=instance.user,
            karma=5
        )
        UserStatistics.objects.filter(pk=instance.user_id).update(
                reviews=F('reviews')+1, karma=F('karma')+5)
        rating_choices = ['one', 'two', 'three', 'four']
        rating = rating_choices[instance.rating-1] + '_star'
        fields = { rating: F(rating)+1, 'reviews': F('reviews')+1 }
        Item.objects.filter(pk=instance.item_id).update(**fields)
        agrees = Agree.objects.filter(
                giver=instance.user_id).order_by('created_at')
        if agrees:
            rating = rating_choices[agrees[0].review.rating-1] + '_star'
            fields = { rating: F(rating)-1 }
            Item.objects.filter(pk=instance.item_id).update(**fields)
            

@receiver(post_delete, sender=Review)
def delete_review(sender, instance, **kwargs):
    """
    Undo the updates when the review was created.
    """
    try:
        Activity.objects.get(
            sender=instance.user,
            verb="raved about",
            object_id=instance.id
        ).delete()
        KarmaAction.objects.filter(
            recipient=instance.user,
            giver=instance.user,
            karma=5,
            created_at__range=(instance.created_at,
                               instance.created_at+dt.timedelta(hours=1))
        )[0].delete()
    except:
        pass

    UserStatistics.objects.filter(pk__exact=instance.user_id).update(
            reviews=F('reviews')-1, karma=F('karma')-5)
    rating_choices = ['one', 'two', 'three', 'four']
    rating = rating_choices[instance.rating-1] + '_star'
    fields = { rating: F(rating)-1, 'reviews': F('reviews')-1 }
    Item.objects.filter(pk=instance.item_id).update(**fields)
    agrees = Agree.objects.filter(
            giver=instance.user_id).order_by('created_at')
    if agrees:
        rating = rating_choices[agrees[0].review.rating-1] + '_star'
        fields = { rating: F(rating)+1 }
        Item.objects.filter(pk=instance.item_id).update(**fields)

@receiver(post_save, sender=Agree)
def create_agree(sender, instance, created, **kwargs):
    """
    Creates a notification for the writer of the review.
    Create two karma actions for the agree.
    Increment the giver's agrees by one and karma by one.
    Increment the receiver's agrees by one and karma by two.
    Increment the item's rating count by one.
    """
    if created:
        Activity.objects.create(
            sender=instance.giver,
            verb="re-raved",
            target_object=instance.review
        )
        Notification.objects.create(
            sender_id=instance.giver_id,
            recipient_id=instance.review.user_id,
            notice_object=instance.review
        )
        KarmaAction.objects.bulk_create([
            KarmaAction(recipient=instance.review.user,
                        giver=instance.giver,
                        karma=2),
            KarmaAction(recipient=instance.giver,
                        giver=instance.giver,
                        karma=1)
        ])
        UserStatistics.objects.filter(pk=instance.giver_id).update(
                agrees_out=F('agrees_out')+1, karma=F('karma')+1)
        UserStatistics.objects.filter(pk=instance.review.user_id).update(
                agrees_in=F('agrees_in')+1, karma=F('karma')+2)
        Review.objects.filter(pk=instance.review_id).update(
                agrees=F('agrees')+1)
        reviews = Review.objects.filter(user=instance.giver_id).count()
        if reviews == 0:
            rating_choices = ['one', 'two', 'three', 'four']
            rating = rating_choices[instance.review.rating-1] + '_star'
            fields = { rating: F(rating)+1 }
            Item.objects.filter(pk=instance.review.item_id).update(
                **fields)
            old_agree = Agree.objects.filter(giver=instance.giver_id) \
                                     .exclude(pk=instance.pk) \
                                     .order_by('-created_at')
            if old_agree:
                rating = (rating_choices[old_agree[0].review.rating-1] +
                    '_star')
                fields = { rating: F(rating)-1 }
                Item.objects.filter(pk=instance.review.item_id).update(
                    **fields)

@receiver(post_delete, sender=Agree)
def delete_agree(sender, instance, **kwargs):
    """
    Undo the updates when the agree was created.
    """
    try:
        Activity.objects.get(
            sender=instance.giver,
            verb="re-raved",
            object_id=instance.review.id
        ).delete()
        Notification.objects.get(
            sender_id=instance.giver_id,
            recipient_id=instance.review.user_id,
            object_id=instance.review.id
        ).delete()
        KarmaAction.objects.filter(
            recipient=instance.review.user,
            giver=instance.giver,
            karma=2,
            created_at__range=(instance.created_at,
                               instance.created_at+dt.timedelta(hours=1))
        )[0].delete()
        KarmaAction.objects.filter(
            recipient=instance.giver,
            giver=instance.giver,
            karma=1,
            created_at__range=(instance.created_at,
                               instance.created_at+dt.timedelta(hours=1))
        )[0].delete()
    except:
        pass

    try:
        UserStatistics.objects.filter(pk=instance.giver_id).update(
                agrees_out=F('agrees_out')-1, karma=F('karma')-1)
        UserStatistics.objects.filter(pk=instance.review.user_id).update(
                agrees_in=F('agrees_in')-1, karma=F('karma')-2)
        Review.objects.filter(pk=instance.review_id).update(
                agrees=F('agrees')-1)
        reviews = Review.objects.filter(user=instance.giver_id).count()
        if reviews == 0:
            remaining = Agree.objects.filter(
                    giver=instance.giver_id).order_by('-created_at')
            if (not remaining or 
                        remaining[0].created_at < instance.created_at):
                rating_choices = ['one', 'two', 'three', 'four']
                rating = (rating_choices[instance.review.rating-1] +
                    '_star')
                fields = { rating: F(rating)-1 }
                Item.objects.filter(pk=instance.review.item_id).update(
                    **fields)
                rating = (rating_choices[remaining[0].review.rating-1] +
                    '_star')
                fields = { rating: F(rating)+1 }
                Item.objects.filter(pk=instance.review.item_id).update(
                    **fields)
    except:
        pass

@receiver(post_save, sender=Thank)
def create_thank(sender, instance, created, **kwargs):
    """
    Create a notification for the writer of the review.
    Create a karma action for the agree.
    Increment the giver's thanks by one and karma by one.
    Increment the receiver's thanks by one and karma by two.
    """
    if created:
        Notification.objects.create(
            sender_id=instance.giver_id,
            recipient_id=instance.review.user_id,
            notice_object=instance.review
        )
        KarmaAction.objects.create(
            recipient=instance.review.user,
            giver=instance.giver,
            karma=1
        )
        UserStatistics.objects.filter(pk=instance.giver_id).update(
                thanks_out=F('thanks_out')+1)
        UserStatistics.objects.filter(pk=instance.review.user_id).update(
                thanks_in=F('thanks_in')+1, karma=F('karma')+1)
        Review.objects.filter(pk=instance.review_id).update(
                thanks=F('thanks')+1)

@receiver(post_delete, sender=Thank)
def delete_thank(sender, instance, **kwargs):
    """
    Undo the updates when the thank was created.
    """
    try:
        Notification.objects.get(
            sender_id=instance.giver_id,
            recipient_id=instance.review.user_id,
            object_id=instance.review.id
        ).delete()
        KarmaAction.objects.filter(
            recipient=instance.review.user,
            giver=instance.giver,
            karma=1,
            created_at__range=(instance.created_at,
                               instance.created_at+dt.timedelta(hours=1))
        )[0].delete()
    except:
        pass
    
    try:
        UserStatistics.objects.filter(pk=instance.giver_id).update(
                thanks_out=F('thanks_out')-1)
        UserStatistics.objects.filter(pk=instance.review.user_id).update(
                thanks_in=F('thanks_in')-1, karma=F('karma')-1)
        Review.objects.filter(pk=instance.review_id).update(
                thanks=F('thanks')-1)
    except:
        pass
