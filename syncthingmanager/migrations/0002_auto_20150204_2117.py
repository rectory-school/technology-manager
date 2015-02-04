# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syncthingmanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StubDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deviceID', models.CharField(unique=True, max_length=63)),
                ('name', models.CharField(max_length=50)),
                ('folders', models.ManyToManyField(to='syncthingmanager.Folder', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='folderpath',
            name='folders',
            field=models.ManyToManyField(to='syncthingmanager.Folder', blank=True),
            preserve_default=True,
        ),
    ]
