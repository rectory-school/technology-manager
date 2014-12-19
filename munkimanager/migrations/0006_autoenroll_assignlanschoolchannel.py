# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0005_auto_20141106_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='autoenroll',
            name='assignLanschoolChannel',
            field=models.BooleanField(default=False, verbose_name=b'Automatically assign a LanSchool Channel'),
            preserve_default=True,
        ),
    ]
