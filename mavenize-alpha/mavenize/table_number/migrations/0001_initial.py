# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'table_number'
        db.create_table('table_number_table_number', (
            ('table_number_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('table_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('table_number', ['table_number'])


    def backwards(self, orm):
        
        # Deleting model 'table_number'
        db.delete_table('table_number_table_number')


    models = {
        'table_number.table_number': {
            'Meta': {'object_name': 'table_number'},
            'table_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'table_number_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['table_number']
