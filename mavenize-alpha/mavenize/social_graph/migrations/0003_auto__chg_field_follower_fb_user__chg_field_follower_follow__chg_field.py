# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Follower.fb_user'
        db.alter_column('social_graph_follower', 'fb_user', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'Follower.follow'
        db.alter_column('social_graph_follower', 'follow', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'Following.fb_user'
        db.alter_column('social_graph_following', 'fb_user', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'Following.follow'
        db.alter_column('social_graph_following', 'follow', self.gf('django.db.models.fields.BigIntegerField')())


    def backwards(self, orm):
        
        # Changing field 'Follower.fb_user'
        db.alter_column('social_graph_follower', 'fb_user', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Follower.follow'
        db.alter_column('social_graph_follower', 'follow', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Following.fb_user'
        db.alter_column('social_graph_following', 'fb_user', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Following.follow'
        db.alter_column('social_graph_following', 'follow', self.gf('django.db.models.fields.IntegerField')())


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
