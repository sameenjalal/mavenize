# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Movie'
        db.create_table('movie_movie', (
            ('movie_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('synopsis', self.gf('django.db.models.fields.TextField')()),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('awards', self.gf('django.db.models.fields.TextField')()),
            ('cast', self.gf('django.db.models.fields.TextField')()),
            ('directors', self.gf('django.db.models.fields.TextField')()),
            ('similars', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('movie', ['Movie'])


    def backwards(self, orm):
        
        # Deleting model 'Movie'
        db.delete_table('movie_movie')


    models = {
        'movie.movie': {
            'Meta': {'object_name': 'Movie'},
            'awards': ('django.db.models.fields.TextField', [], {}),
            'cast': ('django.db.models.fields.TextField', [], {}),
            'directors': ('django.db.models.fields.TextField', [], {}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'movie_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'similars': ('django.db.models.fields.TextField', [], {}),
            'synopsis': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['movie']
