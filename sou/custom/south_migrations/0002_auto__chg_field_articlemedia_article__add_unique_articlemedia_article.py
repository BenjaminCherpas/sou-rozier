# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ArticleMedia.article'
        db.alter_column(u'custom_articlemedia', 'article_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['basic_cms.Article'], unique=True))
        # Adding unique constraint on 'ArticleMedia', fields ['article']
        db.create_unique(u'custom_articlemedia', ['article_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ArticleMedia', fields ['article']
        db.delete_unique(u'custom_articlemedia', ['article_id'])


        # Changing field 'ArticleMedia.article'
        db.alter_column(u'custom_articlemedia', 'article_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['basic_cms.Article']))

    models = {
        u'basic_cms.article': {
            'Meta': {'object_name': 'Article'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'basic_cms_article_rel'", 'null': 'True', 'blank': 'True', 'to': u"orm['coop_cms.ArticleCategory']"}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'headline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'homepage_for_site': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'homepage_article'", 'null': 'True', 'blank': 'True', 'to': u"orm['sites.Site']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'publication': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 12, 15, 0, 0)'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'default': '[2]', 'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'subtitle': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'temp_logo': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        u'coop_cms.articlecategory': {
            'Meta': {'object_name': 'ArticleCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_rss': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'default': '[2]', 'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '100', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'})
        },
        u'coop_cms.mediafilter': {
            'Meta': {'object_name': 'MediaFilter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'custom.articlemedia': {
            'Meta': {'object_name': 'ArticleMedia'},
            'article': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['basic_cms.Article']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_filter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coop_cms.MediaFilter']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['custom']