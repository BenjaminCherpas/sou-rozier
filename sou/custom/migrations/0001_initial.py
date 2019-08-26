# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coop_cms', '0003_auto_20160204_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article', models.OneToOneField(to='basic_cms.Article')),
                ('media_filter', models.ForeignKey(to='coop_cms.MediaFilter')),
            ],
        ),
    ]
