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

    def test_review(self):
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
    
    def test_agree(self):
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

    def test_agree_rating(self):
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        before_first_agree = Item.objects.get(pk=self.item.id).one_star

        self.first_agree = Agree.objects.create(
            giver=self.giver, review=self.review)
        after_first_agree = Item.objects.get(pk=self.item.id).one_star

        # Tests that the item's rating count is incremented by one
        nt.assert_equal(before_first_agree+1, after_first_agree)
    
        self.second_agree = Agree.objects.create(
            giver=self.giver, review=self.review)
        after_second_agree = Item.objects.get(pk=self.item.id).one_star

        # Tests that the item's rating count is not incremented again
        nt.assert_equal(after_first_agree, after_second_agree)

        after_first_delete = Item.objects.get(pk=self.item.id).one_star
        self.first_agree.delete()

        # Tests that the item's rating count is not decremented
        nt.assert_equal(after_second_agree, after_first_delete)
    
        self.second_agree.delete()

        # Tests that the item's rating count is decremented by one
        nt.assert_equal(after_first_delete-1, 
            Item.objects.get(pk=self.item.id).one_star)
            
        self.review.delete()
       
    def test_thank(self):
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
 
    def teardown(self):
        self.writer.delete()
        self.giver.delete()
        self.item.delete()
