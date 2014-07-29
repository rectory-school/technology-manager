# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0006_auto_20140729_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='addedAt',
            field=models.DateTimeField(default=datetime.datetime(2014, 7, 29, 19, 0, 33, 125599), auto_now_add=True),
            preserve_default=False,
        ),
    ]
