# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Genre'
        db.create_table('movie_genre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('movie', ['Genre'])

        # Adding field 'Movie.genre'
        db.add_column('movie_movie', 'genre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['movie.Genre'], null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Genre'
        db.delete_table('movie_genre')

        # Deleting field 'Movie.genre'
        db.delete_column('movie_movie', 'genre_id')


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
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['movie.Genre']", 'null': 'True'}),
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
