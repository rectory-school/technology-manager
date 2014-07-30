# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0012_auto_20140730_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='autoenroll',
            name='enrollmentAllowed',
            field=models.BooleanField(default=True, verbose_name=b'Allow web enrollment'),
            preserve_default=True,
        ),
    ]
