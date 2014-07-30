# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0007_computer_addedat'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='computer',
            name='disabled',
        ),
    ]
