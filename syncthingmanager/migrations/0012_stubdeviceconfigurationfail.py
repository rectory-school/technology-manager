# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syncthingmanager', '0011_masterignoreline'),
    ]

    operations = [
        migrations.CreateModel(
            name='StubDeviceConfigurationFail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_id', models.CharField(max_length=63)),
                ('device_name', models.CharField(max_length=50, blank=True)),
                ('user_name', models.CharField(max_length=50, blank=True)),
                ('ip', models.GenericIPAddressField(null=True, blank=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
