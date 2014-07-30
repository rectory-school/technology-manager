# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0011_auto_20140730_1450'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autoenroll',
            options={'verbose_name': b'Enrollment Set', 'verbose_name_plural': b'Enrollment Sets'},
        ),
        migrations.AlterField(
            model_name='computer',
            name='enrollmentSet',
            field=models.ForeignKey(verbose_name=b'Enrollment Set', blank=True, to='munkimanager.AutoEnroll', null=True),
        ),
    ]
