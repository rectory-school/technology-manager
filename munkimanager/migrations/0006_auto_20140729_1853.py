# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0005_auto_20140729_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='autoenroll',
            name='requireComputerName',
            field=models.BooleanField(default=False, verbose_name=b'Require Computer Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='autoenroll',
            name='requireLanschool',
            field=models.BooleanField(default=False, verbose_name=b'Require LanSchool Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='autoenroll',
            name='setDisabled',
            field=models.BooleanField(default=True, verbose_name=b'Disable on import'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='computer',
            name='disabled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
