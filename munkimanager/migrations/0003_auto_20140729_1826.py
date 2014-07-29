# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0002_auto_20140729_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoLocalUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fullName', models.CharField(max_length=100)),
                ('userName', models.CharField(max_length=20)),
                ('admin', models.BooleanField(default=False)),
                ('forcePasswordReset', models.BooleanField(default=False)),
                ('computer', models.ForeignKey(to='munkimanager.Computer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='catalog',
            options={'ordering': [b'name']},
        ),
        migrations.AlterModelOptions(
            name='computer',
            options={'ordering': [b'computerName', b'serialNumber']},
        ),
        migrations.AlterModelOptions(
            name='installable',
            options={'ordering': [b'name']},
        ),
        migrations.AlterModelOptions(
            name='staticmanifest',
            options={'ordering': [b'manifestName']},
        ),
    ]
