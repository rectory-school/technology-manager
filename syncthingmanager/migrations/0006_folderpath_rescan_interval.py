# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syncthingmanager', '0005_auto_20150205_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='folderpath',
            name='rescan_interval',
            field=models.IntegerField(default=60),
            preserve_default=True,
        ),
    ]
