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
            'reviews': self.writer.get_statistics().reviews,
            'karma': self.writer.get_statistics().karma,
            'one_star': self.item.one_star
        }
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        after_create = dict(UserStatistics.objects.filter(
            pk__exact=self.writer.id).values()[0])

        nt.assert_equal(before_create['reviews']+1,
            after_create['reviews'])
        nt.assert_less(before_create['karma'],
            after_create['karma'])
        nt.assert_equal(before_create['one_star']+1,
            Item.objects.get(pk=self.item.id).one_star)

        self.review.delete()
        after_delete = dict(UserStatistics.objects.filter(
            pk__exact=self.writer.id).values()[0])

        nt.assert_equal(before_create['reviews'],
            after_delete['reviews'])
        nt.assert_equal(before_create['karma'],
            after_delete['karma'])
        nt.assert_equal(before_create['one_star'],
            Item.objects.get(pk=self.item.id).one_star)
    
    def test_agree(self):
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        ids = [self.giver.id, self.review.user.id]

        query = UserStatistics.objects.filter(
            pk__in=ids).order_by('-pk').values()
        before_create = [dict(query[0]), dict(query[1])]
        self.agree = Agree.objects.create(
            giver=self.giver, review=self.review)
        after_create = [dict(query[0]), dict(query[1])]
        
        nt.assert_equal(before_create[0]['agrees_out']+1,
            after_create[0]['agrees_out'])
        nt.assert_less(before_create[0]['karma'],
            after_create[0]['karma'])
        nt.assert_equal(before_create[1]['agrees_in']+1,
            after_create[1]['agrees_in'])
        nt.assert_less(before_create[1]['karma'],
            after_create[1]['karma'])
        
        self.agree.delete()
        after_delete = [dict(query[0]), dict(query[1])]

        nt.assert_equal(after_create[0]['agrees_out']-1,
            after_delete[0]['agrees_out'])
        nt.assert_greater(after_create[0]['karma'],
            after_delete[0]['karma'])
        nt.assert_equal(after_create[1]['agrees_in']-1,
            after_delete[1]['agrees_in'])
        nt.assert_greater(after_create[1]['karma'],
            after_delete[1]['karma'])

        self.review.delete()
       
    def test_thank(self):
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)
        ids = [self.giver.id, self.review.user.id]

        query = UserStatistics.objects.filter(
            pk__in=ids).order_by('-pk').values()
        before_create = [dict(query[0]), dict(query[1])]
        self.thank = Thank.objects.create(
            giver=self.giver, review=self.review)
        after_create = [dict(query[0]), dict(query[1])]
        
        nt.assert_equal(before_create[0]['thanks_out']+1,
            after_create[0]['thanks_out'])
        nt.assert_less(before_create[0]['karma'],
            after_create[0]['karma'])
        nt.assert_equal(before_create[1]['thanks_in']+1,
            after_create[1]['thanks_in'])
        nt.assert_less(before_create[1]['karma'],
            after_create[1]['karma'])
        
        self.thank.delete()
        after_delete = [dict(query[0]), dict(query[1])]

        nt.assert_equal(after_create[0]['thanks_out']-1,
            after_delete[0]['thanks_out'])
        nt.assert_greater(after_create[0]['karma'],
            after_delete[0]['karma'])
        nt.assert_equal(after_create[1]['thanks_in']-1,
            after_delete[1]['thanks_in'])
        nt.assert_greater(after_create[1]['karma'],
            after_delete[1]['karma'])

        self.review.delete()
 
    def teardown(self):
        self.writer.delete()
        self.giver.delete()
        self.item.delete()
