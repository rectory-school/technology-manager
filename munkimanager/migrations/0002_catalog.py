# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('name', models.CharField(max_length=254, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
