# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0008_auto_20140730_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='autoenroll',
            name='setEnabled',
            field=models.BooleanField(default=False, verbose_name=b'Enable on import'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='autoenroll',
            name='setDisabled',
        ),
    ]
