# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AutoEnroll',
            fields=[
                ('name', models.CharField(max_length=100, serialize=False, verbose_name=b'Name', primary_key=True)),
                ('requireLanschool', models.BooleanField(default=False, verbose_name=b'Require LanSchool Name')),
                ('requireComputerName', models.BooleanField(default=False, verbose_name=b'Require Computer Name')),
                ('setEnabled', models.BooleanField(default=False, verbose_name=b'Enable on import')),
                ('enrollmentAllowed', models.BooleanField(default=True, verbose_name=b'Allow web enrollment')),
            ],
            options={
                'verbose_name': b'Enrollment Set',
                'verbose_name_plural': b'Enrollment Sets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AutoLocalUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fullName', models.CharField(max_length=100, verbose_name=b'Full Name')),
                ('userName', models.CharField(max_length=20, verbose_name=b'Username')),
                ('admin', models.BooleanField(default=False, verbose_name=b'Admin')),
                ('forcePasswordReset', models.BooleanField(default=False, verbose_name=b'Force Password Reset')),
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
                'ordering': [b'name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='autoenroll',
            name='catalogs',
            field=models.ManyToManyField(to='munkimanager.Catalog', blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('serialNumber', models.CharField(max_length=100, serialize=False, verbose_name=b'Serial Number', primary_key=True)),
                ('lanschoolName', models.CharField(max_length=200, verbose_name=b'LanSchool Computer Name', blank=True)),
                ('computerName', models.CharField(max_length=50, verbose_name=b'Computer Name', blank=True)),
                ('enabled', models.BooleanField(default=True)),
                ('addedAt', models.DateTimeField(auto_now_add=True)),
                ('lastGrabbed', models.DateTimeField(null=True, blank=True)),
                ('description', models.CharField(max_length=400, blank=True)),
                ('catalogs', models.ManyToManyField(to='munkimanager.Catalog', blank=True)),
                ('enrollmentSet', models.ForeignKey(verbose_name=b'Enrollment Set', blank=True, to='munkimanager.AutoEnroll', null=True)),
            ],
            options={
                'ordering': [b'computerName', b'lanschoolName', b'description', b'serialNumber'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='autolocaluser',
            name='computer',
            field=models.ForeignKey(to='munkimanager.Computer'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Installable',
            fields=[
                ('name', models.CharField(max_length=400, serialize=False, primary_key=True)),
                ('displayName', models.CharField(max_length=400, blank=True)),
                ('uninstallable', models.BooleanField(default=False)),
                ('catalogs', models.ManyToManyField(to='munkimanager.Catalog')),
            ],
            options={
                'ordering': [b'name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='computer',
            name='optionalInstalls',
            field=models.ManyToManyField(to='munkimanager.Installable', verbose_name=b'Optional Installs', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='computer',
            name='managedUninstalls',
            field=models.ManyToManyField(to='munkimanager.Installable', verbose_name=b'Managed Uninstalls', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='computer',
            name='managedInstalls',
            field=models.ManyToManyField(to='munkimanager.Installable', verbose_name=b'Managed Installs', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='autoenroll',
            name='selectableInstalls',
            field=models.ManyToManyField(to='munkimanager.Installable', verbose_name=b'Web Selectable Installs', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='autoenroll',
            name='optionalInstalls',
            field=models.ManyToManyField(to='munkimanager.Installable', verbose_name=b'Optional Installs', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='autoenroll',
            name='managedUninstalls',
            field=models.ManyToManyField(to='munkimanager.Installable', verbose_name=b'Managed Uninstalls', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='autoenroll',
            name='managedInstalls',
            field=models.ManyToManyField(to='munkimanager.Installable', verbose_name=b'Managed Installs', blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='LanSchoolNameOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lanschoolName', models.CharField(max_length=100, verbose_name=b'Lanschool Name')),
            ],
            options={
                'ordering': [b'lanschoolName'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StaticManifest',
            fields=[
                ('manifestName', models.CharField(max_length=100, serialize=False, verbose_name=b'Mainfest Name', primary_key=True)),
                ('description', models.CharField(max_length=200, blank=True)),
                ('catalogs', models.ManyToManyField(to='munkimanager.Catalog')),
                ('includedManifests', models.ManyToManyField(to='munkimanager.StaticManifest', verbose_name=b'Included Manifests', blank=True)),
                ('managedInstalls', models.ManyToManyField(to='munkimanager.Installable', verbose_name=b'Managed Installs', blank=True)),
                ('managedUninstalls', models.ManyToManyField(to='munkimanager.Installable', verbose_name=b'Managed Uninstalls', blank=True)),
                ('optionalInstalls', models.ManyToManyField(to='munkimanager.Installable', verbose_name=b'Optional Installs', blank=True)),
            ],
            options={
                'ordering': [b'manifestName'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='computer',
            name='includedManifests',
            field=models.ManyToManyField(to='munkimanager.StaticManifest', verbose_name=b'Included Manifests', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='autoenroll',
            name='includedManifests',
            field=models.ManyToManyField(to='munkimanager.StaticManifest', verbose_name=b'Included Manifests', blank=True),
            preserve_default=True,
        ),
    ]
