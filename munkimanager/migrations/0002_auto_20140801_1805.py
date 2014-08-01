# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='autolocaluser',
            name='userIcon',
            field=models.ImageField(default='', upload_to=b'', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='staticmanifest',
            name='catalogs',
            field=models.ManyToManyField(to=b'munkimanager.Catalog', blank=True),
        ),
    ]
