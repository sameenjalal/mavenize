from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F

from item.models import Item
from activity_feed.models import Activity
from notification.models import Notification
from user_profile.models import UserStatistics

class Review(models.Model):
    RATING_CHOICES = [(i,i) for i in range(1,6)] 

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
        return "%s agreeing with Review #:%s" % \
            (self.giver.get_full_name(), self.review.id)

class Thank(models.Model):
    giver = models.ForeignKey(User)
    review = models.ForeignKey(Review)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s thanking Review #:%s" % \
            (self.giver.get_full_name(), self.review.id)

@receiver(post_save, sender=Review)
def create_review(sender, instance, created, **kwargs):
    """
    Create an activity for the review.
    Increment the user's reviews by one and karma by five.
    Increment the item's ratings by the review's rating.
    """
    if created:
        Activity.objects.create(
           sender=instance.user,
           verb="raved about",
           target_object=instance
        )    
        UserStatistics.objects.filter(pk__exact=instance.user_id).update(
            reviews=F('reviews')+1, karma=F('karma')+5)
        ratings = ['one', 'two', 'three', 'four', 'five']
        field = ratings[instance.rating-1] + '_star'
        setattr(instance.item, field, F(field)+1)
        instance.item.reviews = F('reviews') + 1
        instance.item.save()

@receiver(post_delete, sender=Review)
def delete_review(sender, instance, **kwargs):
    """
    Undo the updates when the review was created.
    """
    try:
        Activity.objects.get(
            sender=instance.user,
            verb="raved about",
            target_object=instance
        ).delete()
    except:
        pass

    UserStatistics.objects.filter(pk__exact=instance.user_id).update(
        reviews=F('reviews')-1, karma=F('karma')-5)
    ratings = ['one', 'two', 'three', 'four', 'five']
    field = ratings[instance.rating-1] + '_star'
    setattr(instance.item, field, F(field)-1)
    instance.item.reviews = F('reviews') - 1
    instance.item.save()

@receiver(post_save, sender=Agree)
def create_agree(sender, instance, created, **kwargs):
    """
    Creates a notification for the writer of the review.
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
        UserStatistics.objects.filter(
            pk__exact=instance.giver_id).update(
                agrees_out=F('agrees_out')+1, karma=F('karma')+1)
        UserStatistics.objects.filter(
            pk__exact=instance.review.user_id).update(
                agrees_in=F('agrees_in')+1, karma=F('karma')+2)
        instance.review.agrees = F('agrees') + 1
        instance.review.save()
        if Agree.objects.filter(giver=instance.giver_id,
                review__item=instance.review.item).count() == 1:
            ratings = ['one', 'two', 'three', 'four', 'five']
            field = ratings[instance.review.rating-1] + '_star'
            setattr(instance.review.item, field, F(field)+1)
            instance.review.item.save()

@receiver(post_delete, sender=Agree)
def delete_agree(sender, instance, **kwargs):
    """
    Undo the updates when the agree was created.
    """
    try:
        Activity.objects.get(
            sender=instance.giver,
            verb="re-raved",
            target_object=instance.review
        ).delete()
        Notification.objects.get(
            sender_id=instance.giver_id,
            recipient_id=instance.review.user_id,
            notice_object=instance.review
        ).delete()
    except:
        pass

    UserStatistics.objects.filter(
        pk__exact=instance.giver_id).update(
            agrees_out=F('agrees_out')-1, karma=F('karma')-1)
    UserStatistics.objects.filter(
        pk__exact=instance.review.user_id).update(
            agrees_in=F('agrees_in')-1, karma=F('karma')-2)
    instance.review.agrees = F('agrees') - 1
    instance.review.save()
    if not Agree.objects.filter(giver=instance.giver_id,
            review__item=instance.review.item):
        ratings = ['one', 'two', 'three', 'four', 'five']
        field = ratings[instance.review.rating-1] + '_star'
        setattr(instance.review.item, field, F(field)-1)
        instance.review.item.save()

@receiver(post_save, sender=Thank)
def create_thank(sender, instance, created, **kwargs):
    """
    Increment the giver's thanks by one and karma by one.
    Increment the receiver's thanks by one and karma by two.
    """
    if created:
        Notification.objects.create(
            sender_id=instance.giver_id,
            recipient_id=instance.review.user_id,
            notice_object=instance.review
        )
        UserStatistics.objects.filter(
            pk__exact=instance.giver_id).update(
                thanks_out=F('thanks_out')+1, karma=F('karma')+1)
        UserStatistics.objects.filter(
            pk__exact=instance.review.user_id).update(
                thanks_in=F('thanks_in')+1, karma=F('karma')+2)
        instance.review.thanks = F('thanks') + 1
        instance.review.save()

@receiver(post_delete, sender=Thank)
def delete_thank(sender, instance, **kwargs):
    """
    Undo the updates when the thank was created.
    """
    try:
        Notification.objects.get(
            sender_id=instance.giver_id,
            recipient_id=instance.review.user_id,
            notice_object=instance.review
        ).delete()
    except:
        pass
    
    UserStatistics.objects.filter(
        pk__exact=instance.giver_id).update(
            thanks_out=F('thanks_out')-1, karma=F('karma')-1)
    UserStatistics.objects.filter(
        pk__exact=instance.review.user_id).update(
            thanks_in=F('thanks_in')-1, karma=F('karma')-2)
    instance.review.thanks = F('thanks') - 1
    instance.review.save()
