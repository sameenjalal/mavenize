from user_profile.models import KarmaUser
from item.models import Item
from review.models import Review, Agree, Thank
from bookmark.models import Bookmark
from leaderboard.models import KarmaAction
from social_graph.models import Backward
import nose.tools as nt

class TestLeaderboard(object):
    def setup(self):
        self.writer = KarmaUser.objects.create(username='a')
        self.giver = KarmaUser.objects.create(username='b')
        self.item = Item.objects.create()
    
    def test_review(self):
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        self.karma_action = KarmaAction.objects.get(pk=1)

        # Tests that the recipient is the writer of the review
        nt.assert_equal(self.karma_action.recipient.id,
            self.writer.id)
        # Tests that the giver is the writer of the review
        nt.assert_equal(self.karma_action.giver.id, self.writer.id)
        # Tests that the karma sent is 5
        nt.assert_equal(self.karma_action.karma, 5)

        self.review.delete()

        # Tests that the karma action has been deleted
        nt.assert_equal(list(KarmaAction.objects.filter(pk=1)), [])

    def test_agree(self):
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        self.agree = Agree.objects.create(
            giver=self.giver, review=self.review)
        self.karma_actions = KarmaAction.objects.filter(
            giver=self.giver)

        # The first karma object which is from giver to writer
        # Tests that the recipient is the writer of the review
        nt.assert_equal(self.karma_actions[0].recipient.id,
            self.writer.id)
        # Tests that the giver is the giver of the agree
        nt.assert_equal(self.karma_actions[0].giver.id,
            self.giver.id)
        # Tests that the karma sent is 2
        nt.assert_equal(self.karma_actions[0].karma, 2)

        # The second karma object which is from giver to giver 
        # Tests that recipient is the giver of the agree
        nt.assert_equal(self.karma_actions[1].recipient.id,
            self.giver.id)
        # Tests that the giver is the giver of the agree
        nt.assert_equal(self.karma_actions[1].giver.id,
            self.giver.id)
        # Tests that the karma sent is 1
        nt.assert_equal(self.karma_actions[1].karma, 1)

        self.agree.delete()

        # Tests that the karma actions have been deleted
        nt.assert_equal(
            list(KarmaAction.objects.filter(giver=self.giver)), [])

        self.review.delete()

    def test_thanks(self):
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        self.thanks = Thank.objects.create(
            giver=self.giver, review=self.review)
        self.karma_action = KarmaAction.objects.get(
            giver=self.giver)

        # Tests that the recipient is the writer of the review
        nt.assert_equal(self.karma_action.recipient.id,
            self.writer.id)
        # Tests that the giver is the giver of the thanks
        nt.assert_equal(self.karma_action.giver.id, self.giver.id)
        # Tests that the karma sent is 1
        nt.assert_equal(self.karma_action.karma, 1)
        
        self.thanks.delete()

        # Tests that the karma action has been deleted
        nt.assert_equal(
            list(KarmaAction.objects.filter(giver=self.giver)), [])

        self.review.delete()

    def teardown(self):
        self.writer.delete()
        self.giver.delete()
        self.item.delete()
