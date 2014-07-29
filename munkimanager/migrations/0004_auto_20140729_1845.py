# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0003_auto_20140729_1826'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoEnroll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'Name')),
                ('includedManifests', models.ManyToManyField(to='munkimanager.StaticManifest', verbose_name=b'Included Manifests', blank=True)),
                ('managedInstalls', models.ManyToManyField(to='munkimanager.Installable', verbose_name=b'Managed Installs', blank=True)),
                ('managedUninstalls', models.ManyToManyField(to='munkimanager.Installable', verbose_name=b'Managed Uninstalls', blank=True)),
                ('optionalInstalls', models.ManyToManyField(to='munkimanager.Installable', verbose_name=b'Optional Installs', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='computer',
            name='enrolledBy',
            field=models.ForeignKey(blank=True, to='munkimanager.AutoEnroll', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='autolocaluser',
            name='admin',
            field=models.BooleanField(default=False, verbose_name=b'Admin'),
        ),
        migrations.AlterField(
            model_name='autolocaluser',
            name='forcePasswordReset',
            field=models.BooleanField(default=False, verbose_name=b'Force Password Reset'),
        ),
        migrations.AlterField(
            model_name='autolocaluser',
            name='fullName',
            field=models.CharField(max_length=100, verbose_name=b'Full Name'),
        ),
        migrations.AlterField(
            model_name='autolocaluser',
            name='userName',
            field=models.CharField(max_length=20, verbose_name=b'Username'),
        ),
    ]
