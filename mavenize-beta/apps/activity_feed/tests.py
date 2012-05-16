from user_profile.models import KarmaUser
from item.models import Item
from review.models import Review, Agree
from activity_feed.models import Activity
import nose.tools as nt

class TestActivity(object):
    def setup(self):
        self.writer = KarmaUser.objects.create(username='a')
        self.giver = KarmaUser.objects.create(username='b')
        self.item = Item.objects.create()
    
    def test_review(self):
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        self.activity = Activity.objects.get(
            sender=self.writer)

        # Tests that the verb is "raved about"
        nt.assert_equal(self.activity.verb, "raved about")
        # Tests that the target object is the review
        nt.assert_equal(self.activity.target_object,
            self.review)

        self.review.delete()

        # Tests that the activity object has been deleted
        nt.assert_equal(
            list(Activity.objects.filter(sender=self.writer)), [])

    def test_agree(self):
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        self.agree = Agree.objects.create(
            giver=self.giver, review=self.review)
        self.activity = Activity.objects.get(
            sender=self.giver)

        # Tests that the verb is "re-raved"
        nt.assert_equal(self.activity.verb, "re-raved")
        # Tests that the target object is the review
        nt.assert_equal(self.activity.target_object,
            self.review)
        
        self.agree.delete()
        
        # Tests that the activity object has been deleted
        nt.assert_equal(
            list(Activity.objects.filter(sender=self.giver)), [])

        self.review.delete()

    def teardown(self):
        self.writer.delete()
        self.giver.delete()
        self.item.delete()
