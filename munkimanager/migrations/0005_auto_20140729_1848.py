# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0004_auto_20140729_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='autoenroll',
            name='catalogs',
            field=models.ManyToManyField(to=b'munkimanager.Catalog'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='computer',
            name='enrolledBy',
            field=models.ForeignKey(verbose_name=b'Auto Enroll Set', blank=True, to='munkimanager.AutoEnroll', null=True),
        ),
    ]
