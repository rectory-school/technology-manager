# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('syncthingmanager', '0009_stubdevice_last_configure_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='FolderIgnore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, editable=False, db_index=True)),
                ('ignore_line', models.CharField(max_length=254)),
                ('folder', adminsortable.fields.SortableForeignKey(to='syncthingmanager.Folder')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
