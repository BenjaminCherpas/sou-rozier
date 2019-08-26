# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Partner'
        db.create_table(u'course_partner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True)),
        ))
        db.send_create_signal(u'course', ['Partner'])


    def backwards(self, orm):
        # Deleting model 'Partner'
        db.delete_table(u'course_partner')


    models = {
        u'course.partner': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Partner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['course']