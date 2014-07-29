# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0001_squashed_0007_auto_20140729_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticmanifest',
            name='includedManifests',
            field=models.ManyToManyField(to=b'munkimanager.StaticManifest', verbose_name=b'Included Manifests', blank=True),
        ),
        migrations.AlterField(
            model_name='staticmanifest',
            name='managedInstalls',
            field=models.ManyToManyField(to=b'munkimanager.Installable', verbose_name=b'Managed Installs', blank=True),
        ),
        migrations.AlterField(
            model_name='staticmanifest',
            name='managedUninstalls',
            field=models.ManyToManyField(to=b'munkimanager.Installable', verbose_name=b'Managed Uninstalls', blank=True),
        ),
        migrations.AlterField(
            model_name='staticmanifest',
            name='optionalInstalls',
            field=models.ManyToManyField(to=b'munkimanager.Installable', verbose_name=b'Optional Installs', blank=True),
        ),
    ]
