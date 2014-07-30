# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0015_auto_20140730_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='LanSchoolNameOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lanschoolName', models.CharField(max_length=100, verbose_name=b'Lanschool Name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
