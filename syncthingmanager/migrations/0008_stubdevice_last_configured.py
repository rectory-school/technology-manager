# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syncthingmanager', '0007_stubdevice_missing_folders'),
    ]

    operations = [
        migrations.AddField(
            model_name='stubdevice',
            name='last_configured',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
