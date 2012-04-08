from django.contrib.auth.models import User
from user_profile.models import KarmaUser
from user_profile.models import UserStatistics
import nose.tools as nt

class TestUserProfile(object):
    def setup(self):
        self.user = User.objects.create(username='a')
        self.karmauser = KarmaUser.objects.create(username='b')

    #def test_create_user(self):
    #    nt.assert_true(self.user.get_profile())
    #    nt.assert_true(UserStatistics.objects.get(pk=self.user.pk))

    #def test_create_karma_user(self):
    #    nt.assert_true(self.karmauser.get_profile())
    #    nt.assert_true(self.karmauser.get_statistics())

    def teardown(self):
        self.user.delete()
        self.karmauser.delete()
