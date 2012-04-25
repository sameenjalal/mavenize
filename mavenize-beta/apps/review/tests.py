from user_profile.models import KarmaUser
from user_profile.models import UserStatistics
from item.models import Item
from review.models import Review
from review.models import Agree
from review.models import Thank
import nose.tools as nt

class TestReview(object):
    def setup(self):
        self.writer = KarmaUser.objects.create(username='a')
        self.giver = KarmaUser.objects.create(username='b')
        self.item = Item.objects.create()

    def test_review_statistics(self):
        """
        Tests the basic statistics aggregation of a review including:
            User Review Count, User Karma, Item Rating Count, Item
            Review Count
        """
        before_create = {
            'user_reviews': self.writer.get_statistics().reviews,
            'user_karma': self.writer.get_statistics().karma,
            'item_one_star': self.item.one_star,
            'item_reviews': self.item.reviews
        }
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        after_create = dict(UserStatistics.objects.filter(
            pk__exact=self.writer.id).values()[0])

        # Tests that the user's review count is incremented by one
        nt.assert_equal(before_create['user_reviews']+1,
            after_create['reviews'])
        # Tests that the user's karma is greater than before
        nt.assert_less(before_create['user_karma'],
            after_create['karma'])
        # Tests that the item's rating count is incremented by one
        nt.assert_equal(before_create['item_one_star']+1,
            Item.objects.get(pk=self.item.id).one_star)
        # Tests that the item's review count is incremented by one
        nt.assert_equal(before_create['item_reviews']+1,
            Item.objects.get(pk=self.item.id).reviews)

        self.review.delete()
        after_delete = dict(UserStatistics.objects.filter(
            pk__exact=self.writer.id).values()[0])

        # Tests that the user's review count is decremented by one
        nt.assert_equal(before_create['user_reviews'],
            after_delete['reviews'])
        # Tests that the user's karma is the same as before
        nt.assert_equal(before_create['user_karma'],
            after_delete['karma'])
        # Tests that the item's rating count is the same as before
        nt.assert_equal(before_create['item_one_star'],
            Item.objects.get(pk=self.item.id).one_star)
        # Tests that the item's review count is the same as before
        nt.assert_equal(before_create['item_reviews'],
            Item.objects.get(pk=self.item.id).reviews)
    
    def test_agree_statistics(self):
        """
        Tests the basic statistics aggregation of an agree including:
            Giver Outgoing Agree Count, Giver Karma, Receiver Incoming
            Agree Count, Receiver Karma, Review Agree Count
        """
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        ids = [self.giver.id, self.review.user.id]

        query = UserStatistics.objects.filter(
            pk__in=ids).order_by('-pk').values()
        before_create = [dict(query[0]), dict(query[1]),
                         Review.objects.get(pk=self.review.id).agrees]
        self.agree = Agree.objects.create(
            giver=self.giver, review=self.review)
        after_create = [dict(query[0]), dict(query[1]),
                        Review.objects.get(pk=self.review.id).agrees]
        
        # Tests that the giver's agree_outs is incremented by one
        nt.assert_equal(before_create[0]['agrees_out']+1,
            after_create[0]['agrees_out'])
        # Tests that the giver's karma is greater than before
        nt.assert_less(before_create[0]['karma'],
            after_create[0]['karma'])
        # Tests that the receiver's agree_ins is incremented by one
        nt.assert_equal(before_create[1]['agrees_in']+1,
            after_create[1]['agrees_in'])
        # Tests that the receiver's karma is greater than before
        nt.assert_less(before_create[1]['karma'],
            after_create[1]['karma'])
        # Tests that the review's agree count is incremented by one
        nt.assert_equal(before_create[2]+1, after_create[2])
        
        self.agree.delete()
        after_delete = [dict(query[0]), dict(query[1]),
                        Review.objects.get(pk=self.review.id).agrees]

        # Tests that the giver's agree_outs is decremented by one
        nt.assert_equal(after_create[0]['agrees_out']-1,
            after_delete[0]['agrees_out'])
        # Tests that the giver's karma is the less than before
        nt.assert_greater(after_create[0]['karma'],
            after_delete[0]['karma'])
        # Tests that the receiver's agree_ins is decremented by one
        nt.assert_equal(after_create[1]['agrees_in']-1,
            after_delete[1]['agrees_in'])
        # Tests that the receiver's karma is less than before
        nt.assert_greater(after_create[1]['karma'],
            after_delete[1]['karma'])
        # Tests that the review's agree count is decremented by one
        nt.assert_equal(after_create[2]-1, after_delete[2])

        self.review.delete()
      
    def test_thank_statistics(self):
        """
        Tests the basic statistics aggregation of a thank including:
            Giver Outgoing Thank Count, Giver Karma, Receiver Incoming
            Thank Count, Receiver Karma, Review Thank Count
        """
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        ids = [self.giver.id, self.review.user.id]

        query = UserStatistics.objects.filter(
            pk__in=ids).order_by('-pk').values()
        before_create = [dict(query[0]), dict(query[1]),
                         Review.objects.get(pk=self.review.id).thanks]
        self.thank = Thank.objects.create(
            giver=self.giver, review=self.review)
        after_create = [dict(query[0]), dict(query[1]),
                        Review.objects.get(pk=self.review.id).thanks]
        
        # Tests that the giver's thanks_outs is incremented by one
        nt.assert_equal(before_create[0]['thanks_out']+1,
            after_create[0]['thanks_out'])
        # Tests that the giver's karma does not change
        nt.assert_equal(before_create[0]['karma'],
            after_create[0]['karma'])
        # Tests that the receiver's thanks_ins is incremented by one
        nt.assert_equal(before_create[1]['thanks_in']+1,
            after_create[1]['thanks_in'])
        # Tests that the receiver's karma is greater than before
        nt.assert_less(before_create[1]['karma'],
            after_create[1]['karma'])
        # Tests that the review's thanks is incremented by one
        nt.assert_equal(before_create[2]+1, after_create[2])
        
        self.thank.delete()
        after_delete = [dict(query[0]), dict(query[1]),
                        Review.objects.get(pk=self.review.id).thanks]

        # Tests that the giver's thanks_outs is decremented by one
        nt.assert_equal(after_create[0]['thanks_out']-1,
            after_delete[0]['thanks_out'])
        # Tests that the giver's karma does not change
        nt.assert_equal(after_create[0]['karma'],
            after_delete[0]['karma'])
        # Tests that the receiver's thanks_ins is decremented by one
        nt.assert_equal(after_create[1]['thanks_in']-1,
            after_delete[1]['thanks_in'])
        # Tests that the receiver's karma is less than before
        nt.assert_greater(after_create[1]['karma'],
            after_delete[1]['karma'])
        # Tests that the review's thanks is decremented by one
        nt.assert_equal(after_create[2]-1, after_delete[2])

        self.review.delete()
    
    def test_rating_after_agree(self):
        """
        Tests that successive agrees overwrites the rating count from
        previous agrees and the most recent overwrites a deleted agree.
        """
        self.review_one = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        self.review_two = Review.objects.create(
            user=self.writer, item=self.item, rating=2)
        before_first_agree = Item.objects.get(pk=self.item.id)

        self.first_agree = Agree.objects.create(
            giver=self.giver, review=self.review_one)
        after_first_agree = Item.objects.get(pk=self.item.id)

        # Tests that the item's rating count is incremented by one
        nt.assert_equal(before_first_agree.one_star+1,
            after_first_agree.one_star)
    
        self.second_agree = Agree.objects.create(
            giver=self.giver, review=self.review_two)
        after_second_agree = Item.objects.get(pk=self.item.id)

        # Tests that the item's rating count has been overwritten
        # by the new agree
        nt.assert_equal(after_first_agree.one_star,
            after_second_agree.one_star+1)
        nt.assert_equal(after_first_agree.two_star,
            after_second_agree.two_star-1)

        self.first_agree.delete()
        after_first_delete = Item.objects.get(pk=self.item.id)

        # Tests that the item's rating count has been unchanged 
        nt.assert_equal(after_second_agree.one_star,
            after_first_delete.one_star)
        nt.assert_equal(after_second_agree.two_star,
            after_first_delete.two_star)
    
        self.second_agree.delete()

        # Tests that the item's rating count is overwritten
        nt.assert_equal(before_first_agree.one_star,
            Item.objects.get(pk=self.item.id).one_star)
        nt.assert_equal(before_first_agree.two_star,
            Item.objects.get(pk=self.item.id).two_star)
            
        self.review_one.delete()
        self.review_two.delete()

    def test_rating_for_review_after_agree(self):
        """
        Tests that the rating is overwritten when a user writes a
        review after they have already agreed with a review on the
        same item.
        """
        self.writer_review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        self.agree = Agree.objects.create(
            giver=self.giver, review=self.writer_review)
        after_agree = Item.objects.get(pk=self.item.id)

        # Tests that the item's one star rating count is two 
        nt.assert_equal(after_agree.one_star, 2)
        
        self.giver_review = Review.objects.create(
            user=self.giver, item=self.item, rating=2)
        after_review = Item.objects.get(pk=self.item.id)

        # Tests that the item's one star rating count is one
        nt.assert_equal(after_review.one_star, 1)
        # Tests that the item's two star rating count is one
        nt.assert_equal(after_review.two_star, 1)

        self.agree.delete()
        after_agree_delete = Item.objects.get(pk=self.item.id)
        
        # Tests that the item's ratings are the same 
        nt.assert_equal(after_review.one_star,
            after_agree_delete.one_star)
        nt.assert_equal(after_review.two_star,
            after_agree_delete.two_star)

        self.giver_review.delete()
        self.writer_review.delete()

    def test_rating_for_agree_after_review(self):
        """
        Tests that the agree does not add a rating if the user has
        already written a review on the same item.
        """
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        before_agree = Item.objects.get(pk=self.item.id)

        self.agree = Agree.objects.create(
            giver=self.writer, review=self.review)
        after_agree = Item.objects.get(pk=self.item.id)

        # Tests that the item's rating count is not incremented
        nt.assert_equal(before_agree.one_star, after_agree.one_star)

        self.agree.delete()
        after_agree_delete = Item.objects.get(pk=self.item.id)
        
        # Tests that the item's rating count is not decremented
        nt.assert_equal(after_agree.one_star,
            after_agree_delete.one_star)

        self.review.delete()

    def test_rating_for_agree_after_deleting_review(self):
        """
        Tests that the agree's rating has replaced the review's
        rating if the review is deleted.
        """
        self.writer_review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)        
        self.agree = Agree.objects.create(
            giver=self.giver, review=self.writer_review)
        after_agree = Item.objects.get(pk=self.item.id)

        self.giver_review = Review.objects.create(
            user=self.giver, item=self.item, rating=2)
        self.giver_review.delete()
        after_review_delete = Item.objects.get(pk=self.item.id)

        # Tests that the rating is unchanged after the review
        # is deleted
        nt.assert_equal(after_agree.one_star,
            after_review_delete.one_star)
        nt.assert_equal(after_agree.two_star,
            after_review_delete.two_star)

        self.agree.delete()
        self.writer_review.delete()

    def teardown(self):
        self.writer.delete()
        self.giver.delete()
        self.item.delete()
