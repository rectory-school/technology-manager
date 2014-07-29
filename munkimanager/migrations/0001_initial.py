# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

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
                ('manifestName', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=200, blank=True)),
                ('includedManifests', models.ManyToManyField(to='munkimanager.StaticManifest', blank=True)),
                ('managedInstalls', models.ManyToManyField(to='munkimanager.Installable')),
                ('managedUninstalls', models.ManyToManyField(to='munkimanager.Installable')),
                ('optionalInstalls', models.ManyToManyField(to='munkimanager.Installable')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
