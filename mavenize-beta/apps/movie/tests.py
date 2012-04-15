from item.models import Item
from movie.models import Movie
import nose.tools as nt

class TestMovie(object):
    def setup(self):
        self.movie = Movie.objects.create(
            item=Item(), runtime=-100, critic_score=94)
        self.id = Movie.objects.get(runtime=self.movie.runtime).pk
    
    def test_create_movie(self):
        nt.assert_true(
            Movie.objects.get(pk=self.id))
        nt.assert_equal(Movie.objects.get(pk=self.id).item.item_type,
            'movie')

    def test_delete_movie(self):
        Movie.objects.get(pk=self.id).delete()
        nt.assert_false(Item.objects.filter(pk=self.id))

    def teardown(self):
        Movie.objects.filter(pk=self.id).delete()
