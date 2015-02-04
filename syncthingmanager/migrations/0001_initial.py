# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('relative_path', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FolderPath',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('local_path', models.CharField(max_length=254)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ManagedDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_name', models.CharField(max_length=50)),
                ('sync_address', models.CharField(max_length=50)),
                ('gui_address', models.URLField(max_length=254)),
                ('deviceID', models.CharField(unique=True, max_length=63)),
                ('apiKey', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='folderpath',
            name='device',
            field=models.ForeignKey(to='syncthingmanager.ManagedDevice'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='folderpath',
            name='folders',
            field=models.ManyToManyField(to='syncthingmanager.Folder'),
            preserve_default=True,
        ),
    ]
