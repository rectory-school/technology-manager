# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0013_autoenroll_enrollmentallowed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autoenroll',
            name='id',
        ),
        migrations.AlterField(
            model_name='autoenroll',
            name='name',
            field=models.CharField(max_length=100, serialize=False, verbose_name=b'Name', primary_key=True),
        ),
    ]
