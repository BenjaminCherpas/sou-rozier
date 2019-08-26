# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_competition_is_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]
