# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syncthingmanager', '0004_auto_20150205_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manageddevice',
            old_name='deviceID',
            new_name='device_id',
        ),
        migrations.RenameField(
            model_name='stubdevice',
            old_name='deviceID',
            new_name='device_id',
        ),
        migrations.RenameField(
            model_name='stubdevice',
            old_name='name',
            new_name='device_name',
        ),
    ]
