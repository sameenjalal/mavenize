# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Follower.follower'
        db.delete_column('social_graph_follower', 'follower')

        # Deleting field 'Follower.user'
        db.delete_column('social_graph_follower', 'user_id')

        # Adding field 'Follower.fb_user'
        db.add_column('social_graph_follower', 'fb_user', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Follower.follow'
        db.add_column('social_graph_follower', 'follow', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'Following.following'
        db.delete_column('social_graph_following', 'following')

        # Deleting field 'Following.user'
        db.delete_column('social_graph_following', 'user_id')

        # Adding field 'Following.fb_user'
        db.add_column('social_graph_following', 'fb_user', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Following.follow'
        db.add_column('social_graph_following', 'follow', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'Follower.follower'
        raise RuntimeError("Cannot reverse this migration. 'Follower.follower' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Follower.user'
        raise RuntimeError("Cannot reverse this migration. 'Follower.user' and its values cannot be restored.")

        # Deleting field 'Follower.fb_user'
        db.delete_column('social_graph_follower', 'fb_user')

        # Deleting field 'Follower.follow'
        db.delete_column('social_graph_follower', 'follow')

        # User chose to not deal with backwards NULL issues for 'Following.following'
        raise RuntimeError("Cannot reverse this migration. 'Following.following' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Following.user'
        raise RuntimeError("Cannot reverse this migration. 'Following.user' and its values cannot be restored.")

        # Deleting field 'Following.fb_user'
        db.delete_column('social_graph_following', 'fb_user')

        # Deleting field 'Following.follow'
        db.delete_column('social_graph_following', 'follow')


    models = {
        'social_graph.follower': {
            'Meta': {'object_name': 'Follower'},
            'fb_user': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'follow': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'social_graph.following': {
            'Meta': {'object_name': 'Following'},
            'fb_user': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'follow': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['social_graph']
