# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Movie.release_date'
        db.alter_column('movie_movie', 'release_date', self.gf('django.db.models.fields.DateField')())


    def backwards(self, orm):
        
        # Changing field 'Movie.release_date'
        db.alter_column('movie_movie', 'release_date', self.gf('django.db.models.fields.DateTimeField')())


    models = {
        'movie.movie': {
            'Meta': {'object_name': 'Movie'},
            'awards': ('django.db.models.fields.TextField', [], {}),
            'cast': ('django.db.models.fields.TextField', [], {}),
            'directors': ('django.db.models.fields.TextField', [], {}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'movie_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {}),
            'similars': ('django.db.models.fields.TextField', [], {}),
            'synopsis': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['movie']
