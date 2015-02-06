# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syncthingmanager', '0006_folderpath_rescan_interval'),
    ]

    operations = [
        migrations.AddField(
            model_name='stubdevice',
            name='missing_folders',
            field=models.ManyToManyField(related_name='missing_on', to='syncthingmanager.Folder'),
            preserve_default=True,
        ),
    ]
