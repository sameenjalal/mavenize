from item.models import Item
from item.models import Popularity
import nose.tools as nt

class TestItem(object):
    def setup(self):
        self.item = Item.objects.create()

    def test_create_item(self):
        nt.assert_true(Popularity.objects.get(pk=self.item.id))

    def test_delete_item(self):
        Item.objects.get(pk=self.item.id).delete()
        nt.assert_false(Popularity.objects.filter(pk=self.item.id))

    def teardown(self):
        Item.objects.filter(pk=self.item.id).delete()
