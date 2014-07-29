# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0003_auto_20140729_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='installable',
            name='catalogs',
            field=models.ManyToManyField(to=b'munkimanager.Catalog'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='staticmanifest',
            name='catalogs',
        ),
    ]
