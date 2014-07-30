# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0014_auto_20140730_1808'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='computer',
            options={'ordering': [b'computerName', b'lanschoolName', b'description', b'serialNumber']},
        ),
        migrations.AlterField(
            model_name='autoenroll',
            name='catalogs',
            field=models.ManyToManyField(to=b'munkimanager.Catalog', blank=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='catalogs',
            field=models.ManyToManyField(to=b'munkimanager.Catalog', blank=True),
        ),
    ]
