# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syncthingmanager', '0003_auto_20150205_1542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manageddevice',
            old_name='apiKey',
            new_name='api_key',
        ),
    ]
