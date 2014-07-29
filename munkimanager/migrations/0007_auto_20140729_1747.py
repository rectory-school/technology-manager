# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0006_staticmanifest_catalogs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='includedManifests',
            field=models.ManyToManyField(to=b'munkimanager.StaticManifest', verbose_name=b'Included Manifests', blank=True),
        ),
    ]
