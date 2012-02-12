# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Movie.genre'
        db.delete_column('movie_movie', 'genre_id')

        # Adding M2M table for field genre on 'Movie'
        db.create_table('movie_movie_genre', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm['movie.movie'], null=False)),
            ('genre', models.ForeignKey(orm['movie.genre'], null=False))
        ))
        db.create_unique('movie_movie_genre', ['movie_id', 'genre_id'])


    def backwards(self, orm):
        
        # Adding field 'Movie.genre'
        db.add_column('movie_movie', 'genre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['movie.Genre'], null=True), keep_default=False)

        # Removing M2M table for field genre on 'Movie'
        db.delete_table('movie_movie_genre')


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
        }
    }

    complete_apps = ['movie']
