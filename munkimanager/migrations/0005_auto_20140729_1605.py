# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0004_auto_20140729_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='computerName',
            field=models.CharField(default='', max_length=50, verbose_name=b'Computer Name', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='computer',
            name='includedManifests',
            field=models.ManyToManyField(to=b'munkimanager.Computer', verbose_name=b'Included Manifests', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='computer',
            name='managedInstalls',
            field=models.ManyToManyField(to=b'munkimanager.Installable', verbose_name=b'Managed Installs', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='computer',
            name='managedUninstalls',
            field=models.ManyToManyField(to=b'munkimanager.Installable', verbose_name=b'Managed Uninstalls', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='computer',
            name='optionalInstalls',
            field=models.ManyToManyField(to=b'munkimanager.Installable', verbose_name=b'Optional Installs', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='computer',
            name='lanschoolName',
            field=models.CharField(max_length=200, verbose_name=b'LanSchool Computer Name', blank=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='serialNumber',
            field=models.CharField(max_length=100, serialize=False, verbose_name=b'Serial Number', primary_key=True),
        ),
        migrations.AlterField(
            model_name='staticmanifest',
            name='managedInstalls',
            field=models.ManyToManyField(to=b'munkimanager.Installable', blank=True),
        ),
        migrations.AlterField(
            model_name='staticmanifest',
            name='managedUninstalls',
            field=models.ManyToManyField(to=b'munkimanager.Installable', blank=True),
        ),
        migrations.AlterField(
            model_name='staticmanifest',
            name='manifestName',
            field=models.CharField(max_length=100, serialize=False, verbose_name=b'Mainfest Name', primary_key=True),
        ),
        migrations.AlterField(
            model_name='staticmanifest',
            name='optionalInstalls',
            field=models.ManyToManyField(to=b'munkimanager.Installable', blank=True),
        ),
    ]
