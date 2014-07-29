# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0005_auto_20140729_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticmanifest',
            name='catalogs',
            field=models.ManyToManyField(to=b'munkimanager.Catalog'),
            preserve_default=True,
        ),
    ]
