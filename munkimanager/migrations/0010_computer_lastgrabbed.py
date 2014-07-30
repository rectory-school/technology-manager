# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0009_auto_20140730_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='lastGrabbed',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
