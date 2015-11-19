# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syncthingmanager', '0012_stubdeviceconfigurationfail'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscoveryServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=254)),
            ],
        ),
    ]
