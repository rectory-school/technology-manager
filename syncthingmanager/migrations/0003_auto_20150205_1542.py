# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syncthingmanager', '0002_auto_20150204_2117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='folder',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='folder',
            name='name',
            field=models.CharField(unique=True, max_length=50),
            preserve_default=True,
        ),
    ]
