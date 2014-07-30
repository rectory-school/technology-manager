# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0016_lanschoolnameoption'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lanschoolnameoption',
            options={'ordering': [b'lanschoolName']},
        ),
        migrations.AddField(
            model_name='autoenroll',
            name='selectableInstalls',
            field=models.ManyToManyField(to=b'munkimanager.Installable', verbose_name=b'Web Selectable Installs', blank=True),
            preserve_default=True,
        ),
    ]
