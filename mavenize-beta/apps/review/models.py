from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from django import forms

from item.models import Item

import datetime as dt
import api
import utils

"""
Models
"""
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
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s thanking Review #%s" % \
            (self.giver.get_full_name(), self.review.id)

"""
Model Forms
"""
class ReviewForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
            'id': 'review-text',
            'placeholder': 'Tell us what you thought, choose a rating, and rave!',
            'rows': 1,
        }))

    class Meta:
        model = Review

class ThankForm(forms.ModelForm):

    class Meta:
        model = Thank

"""
Signals
"""
@receiver(post_save, sender=Review)
def create_review(sender, instance, created, **kwargs):
    """
    Queue an activity for the review.
    Create a karma action for the review.
    Increment the user's reviews by one and karma by five.
    Update the item's ratings by the review's rating.
    Update the item's popularity by the review's rating.
    """
    if created:
        api.queue_activity(
            sender_id=instance.user_id, 
            verb="raved about",
            model_name="review",
            obj_id=instance.pk
        )
        api.add_karma_action(
            recipient_id=instance.user_id,
            giver_id=instance.user_id,
            karma=5
        )
        api.update_statistics(
            model_name="userstatistics",
            obj_id=instance.user_id,
            reviews=1,
            karma=5
        )
        rating = utils.get_rating_field(instance.rating)
        api.update_statistics(
            model_name="item",
            obj_id=instance.item_id,
            **{ rating: 1, 'reviews': 1 }
        )
        api.update_statistics(
            model_name="popularity",
            obj_id=instance.item_id,
            today=instance.rating,
            week=instance.rating,
            month=instance.rating,
            alltime=instance.rating
        )
        agrees = api.filter_then_order_by(
            model_name="agree",
            order_criteria="-created_at",
            giver=instance.user_id,
            review__item=instance.item_id
        )
        if agrees:
            rating = utils.get_rating_field(agrees[0].review.rating)
            api.update_statistics(
                model_name="item",
                obj_id=instance.item_id,
                **{ rating: -1}
            )
            

@receiver(post_delete, sender=Review)
def delete_review(sender, instance, **kwargs):
    """
    Deletes all related activities, agrees, and thanks.
    Undo the updates when the review was created.
    """
    api.filter_then_delete(
        model_name="activity",
        content_type=api.get_content_type("review"),
        object_id=instance.pk
    )
    api.filter_then_delete(model_name="agree", review=instance.pk)
    api.filter_then_delete(model_name="thank", review=instance.pk)
    api.update_statistics(
        model_name="userstatistics",
        obj_id=instance.user_id,
        reviews=-1,
        karma=-5
    )
    rating = utils.get_rating_field(instance.rating)
    api.update_statistics(
        model_name="item",
        obj_id=instance.item_id,
        **{ rating: -1, 'reviews': -1 }
    )
    api.update_statistics(
        model_name="popularity",
        obj_id=instance.item_id,
        **utils.decrement_popularities(instance.created_at,
            instance.rating)
    )
    agrees = api.filter_then_order_by(
        model_name="agree",
        order_criteria="-created_at",
        giver=instance.user_id,
        review__item=instance.item_id
    )
    if agrees:
        rating = utils.get_rating_field(agrees[0].review.rating)
        api.update_statistics(
            model_name="item",
            obj_id=instance.item_id,
            **{ rating: 1 }
        )

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
        api.queue_activity(
            sender_id=instance.giver_id,
            verb="re-raved",
            model_name="review",
            obj_id=instance.review_id
        )
        api.queue_notification(
            sender_id=instance.giver_id,
            recipient_id=instance.review.user_id,
            model_name="agree",
            obj_id=instance.pk
        )
        api.add_karma_action(
            recipient_id=instance.review.user_id,
            giver_id=instance.giver_id,
            karma=2
        )
        api.add_karma_action(
            recipient_id=instance.giver_id,
            giver_id=instance.giver_id,
            karma=1
        )
        api.update_statistics(
            model_name="userstatistics",
            obj_id=instance.giver_id,
            agrees_out=1,
            karma=1
        )
        api.update_statistics(
            model_name="userstatistics",
            obj_id=instance.review.user_id,
            agrees_in=1,
            karma=2
        )
        api.update_statistics(
            model_name="review",
            obj_id=instance.review_id,
            agrees=1
        )
        api.update_statistics(
            model_name="popularity",
            obj_id=instance.review.item_id,
            today=instance.review.rating,
            week=instance.review.rating,
            month=instance.review.rating,
            alltime=instance.review.rating
        )
        reviews = api.filter_then_count(
            model_name="review",
            user=instance.giver_id,
            item=instance.review.item_id
        )
        if reviews == 0:
            rating = utils.get_rating_field(instance.review.rating)
            api.update_statistics(
                model_name="item",
                obj_id=instance.review.item_id,
                **{ rating: 1}
            )
            old_agrees = api.filter_excluding_me_then_order_by(
                model_name="agree",
                obj_id=instance.pk,
                order_criteria="-created_at",
                giver=instance.giver_id,
                review__item=instance.review.item_id
            )
            if old_agrees:
                rating = utils.get_rating_field(
                                old_agrees[0].review.rating)
                api.update_statistics(
                    model_name="item",
                    obj_id=instance.review.item_id,
                    **{ rating: -1 }
                )

@receiver(post_delete, sender=Agree)
def delete_agree(sender, instance, **kwargs):
    """
    Undo the updates when the agree was created.
    """
    api.remove_activity(
        sender_id=instance.giver_id,
        verb="re-raved",
        model_name="review",
        obj_id=instance.review_id
    )
    api.remove_notification(
        sender_id=instance.giver_id,
        recipient_id=instance.review.user_id,
        model_name="agree",
        obj_id=instance.pk
    )
    api.remove_karma_action(
        recipient_id=instance.review.user_id,
        giver_id=instance.giver_id,
        karma=2,
        time_range=(instance.created_at,
                    instance.created_at+dt.timedelta(hours=1))
    )
    api.remove_karma_action(
        recipient_id=instance.giver_id,
        giver_id=instance.giver_id,
        karma=1,
        time_range=(instance.created_at,
                    instance.created_at+dt.timedelta(hours=1))
    )
    api.update_statistics(
       model_name="userstatistics",
       obj_id=instance.giver_id,
       agrees_out=-1,
       karma=-1
    )
    api.update_statistics(
        model_name="userstatistics",
        obj_id=instance.review.user_id,
        agrees_in=-1,
        karma=-2
    )
    api.update_statistics(
        model_name="review",
        obj_id=instance.review_id,
        agrees=-1
    )
    api.update_statistics(
        model_name="popularity",
        obj_id=instance.review.item_id,
        **utils.decrement_popularities(instance.created_at,
            instance.review.rating)
    )
    reviews = api.filter_then_count(
        model_name="review",
        user=instance.giver_id,
        item=instance.review.item_id
    )
    if reviews == 0:
        remaining = api.filter_then_order_by(
            model_name="agree",
            order_criteria="-created_at",
            giver=instance.giver_id,
            review__item=instance.review.item_id
        )
        if (not remaining or 
                    remaining[0].created_at < instance.created_at):
            old_rating = utils.get_rating_field(instance.review.rating)
            api.update_statistics(
                model_name="item",
                obj_id=instance.review.item_id,
                **{ old_rating: -1 }
            )
            if remaining:
                new_rating = utils.get_rating_field(
                    remaining[0].review.rating)
                api.update_statistics(
                    model_name="item",
                    obj_id=instance.review.item_id,
                    **{ new_rating: 1 }
                )

@receiver(post_save, sender=Thank)
def create_thank(sender, instance, created, **kwargs):
    """
    Create a notification for the writer of the review.
    Create a karma action for the agree.
    Increment the giver's thanks by one and karma by one.
    Increment the receiver's thanks by one and karma by two.
    """
    if created:
        api.queue_notification(
            sender_id=instance.giver_id,
            recipient_id=instance.review.user_id,
            model_name="thank",
            obj_id=instance.pk
        )
        api.add_karma_action(
            recipient_id=instance.review.user_id,
            giver_id=instance.giver_id,
            karma=1
        )
        api.update_statistics(
            model_name="userstatistics",
            obj_id=instance.giver_id,
            thanks_out=1
        )
        api.update_statistics(
            model_name="userstatistics",
            obj_id=instance.review.user_id,
            thanks_in=1,
            karma=1
        )
        api.update_statistics(
            model_name="review",
            obj_id=instance.review_id,
            thanks=1
        )
        api.update_statistics(
            model_name="popularity",
            obj_id=instance.review.item_id,
            today=instance.review.rating,
            week=instance.review.rating,
            month=instance.review.rating,
            alltime=instance.review.rating
        )

@receiver(post_delete, sender=Thank)
def delete_thank(sender, instance, **kwargs):
    """
    Undo the updates when the thank was created.
    """
    api.remove_notification(
        sender_id=instance.giver_id,
        recipient_id=instance.review.user_id,
        model_name="thank",
        obj_id=instance.pk
    )
    api.remove_karma_action(
        recipient_id=instance.review.user_id,
        giver_id=instance.giver_id,
        karma=1,
        time_range=(instance.created_at,
                    instance.created_at+dt.timedelta(hours=1))
    )
    api.update_statistics(
        model_name="userstatistics",
        obj_id=instance.giver_id,
        thanks_out=-1
    )
    api.update_statistics(
        model_name="userstatistics",
        obj_id=instance.review.user_id,
        thanks_in=-1,
        karma=-1
    )
    api.update_statistics(
        model_name="review",
        obj_id=instance.review_id,
        thanks=-1
    )
    api.update_statistics(
        model_name="popularity",
        obj_id=instance.review.item_id,
        **utils.decrement_popularities(instance.created_at,
            instance.review.rating)
    )
