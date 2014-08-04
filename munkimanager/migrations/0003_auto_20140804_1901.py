# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0002_auto_20140801_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='lanschoolChannel',
            field=models.IntegerField(null=True, verbose_name=b'LanSchool Channel', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='autolocaluser',
            name='userIcon',
            field=models.ImageField(upload_to=b'', verbose_name=b'User Icon', blank=True),
        ),
    ]
