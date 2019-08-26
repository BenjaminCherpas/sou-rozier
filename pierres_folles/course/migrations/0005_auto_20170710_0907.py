# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_auto_20160725_2257'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('ordering', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('ordering',),
                'verbose_name': "Source d'information",
                'verbose_name_plural': "Source d'informations",
            },
        ),
        migrations.AddField(
            model_name='partner',
            name='best_partner',
            field=models.BooleanField(default=False, verbose_name='partenaire majeur'),
        ),
        migrations.AddField(
            model_name='partner',
            name='ordering',
            field=models.IntegerField(default=0, verbose_name="order d'affichage"),
        ),
        migrations.AddField(
            model_name='runner',
            name='source_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='course.InfoSource', null=True),
        ),
    ]
