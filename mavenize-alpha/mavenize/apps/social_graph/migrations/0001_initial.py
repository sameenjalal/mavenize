# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Following'
        db.create_table('social_graph_following', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fb_user', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('follow', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('social_graph', ['Following'])

        # Adding model 'Follower'
        db.create_table('social_graph_follower', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fb_user', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('follow', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('social_graph', ['Follower'])


    def backwards(self, orm):
        
        # Deleting model 'Following'
        db.delete_table('social_graph_following')

        # Deleting model 'Follower'
        db.delete_table('social_graph_follower')


    models = {
        'social_graph.follower': {
            'Meta': {'object_name': 'Follower'},
            'fb_user': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'follow': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'social_graph.following': {
            'Meta': {'object_name': 'Following'},
            'fb_user': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'follow': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['social_graph']
