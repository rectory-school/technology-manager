# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [(b'munkimanager', '0001_initial'), (b'munkimanager', '0002_catalog'), (b'munkimanager', '0003_auto_20140729_1451'), (b'munkimanager', '0004_auto_20140729_1457'), (b'munkimanager', '0005_auto_20140729_1605'), (b'munkimanager', '0006_staticmanifest_catalogs'), (b'munkimanager', '0007_auto_20140729_1747')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('serialNumber', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('lanschoolName', models.CharField(max_length=200, blank=True)),
                ('description', models.CharField(max_length=400, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Installable',
            fields=[
                ('name', models.CharField(max_length=400, serialize=False, primary_key=True)),
                ('displayName', models.CharField(max_length=400, blank=True)),
                ('uninstallable', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StaticManifest',
            fields=[
                ('manifestName', models.CharField(max_length=100, serialize=False, verbose_name=b'Mainfest Name', primary_key=True)),
                ('description', models.CharField(max_length=200, blank=True)),
                ('includedManifests', models.ManyToManyField(to=b'munkimanager.StaticManifest', blank=True)),
                ('managedInstalls', models.ManyToManyField(to=b'munkimanager.Installable', blank=True)),
                ('managedUninstalls', models.ManyToManyField(to=b'munkimanager.Installable', blank=True)),
                ('optionalInstalls', models.ManyToManyField(to=b'munkimanager.Installable', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('name', models.CharField(max_length=254, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='computer',
            name='catalogs',
            field=models.ManyToManyField(to=b'munkimanager.Catalog'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='installable',
            name='catalogs',
            field=models.ManyToManyField(to=b'munkimanager.Catalog'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='computer',
            name='computerName',
            field=models.CharField(default='', max_length=50, verbose_name=b'Computer Name', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='computer',
            name='includedManifests',
            field=models.ManyToManyField(to=b'munkimanager.StaticManifest', verbose_name=b'Included Manifests', blank=True),
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
        migrations.AddField(
            model_name='staticmanifest',
            name='catalogs',
            field=models.ManyToManyField(to=b'munkimanager.Catalog'),
            preserve_default=True,
        ),
    ]
