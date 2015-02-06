# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syncthingmanager', '0008_stubdevice_last_configured'),
    ]

    operations = [
        migrations.AddField(
            model_name='stubdevice',
            name='last_configure_result',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
