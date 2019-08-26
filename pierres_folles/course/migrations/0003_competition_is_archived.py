# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_partner_is_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='is_archived',
            field=models.BooleanField(default=True),
        ),
    ]
