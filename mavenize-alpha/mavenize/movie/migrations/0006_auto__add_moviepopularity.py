# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MoviePopularity'
        db.create_table('movie_moviepopularity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('movie', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['movie.Movie'], unique=True)),
            ('popularity', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('movie', ['MoviePopularity'])


    def backwards(self, orm):
        
        # Deleting model 'MoviePopularity'
        db.delete_table('movie_moviepopularity')


    models = {
        'movie.genre': {
            'Meta': {'object_name': 'Genre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'movie.movie': {
            'Meta': {'object_name': 'Movie'},
            'awards': ('django.db.models.fields.TextField', [], {}),
            'cast': ('django.db.models.fields.TextField', [], {}),
            'directors': ('django.db.models.fields.TextField', [], {}),
            'genre': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['movie.Genre']", 'null': 'True', 'symmetrical': 'False'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'movie_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {}),
            'similars': ('django.db.models.fields.TextField', [], {}),
            'synopsis': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'movie.moviepopularity': {
            'Meta': {'object_name': 'MoviePopularity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['movie.Movie']", 'unique': 'True'}),
            'popularity': ('django.db.models.fields.BigIntegerField', [], {})
        }
    }

    complete_apps = ['movie']
