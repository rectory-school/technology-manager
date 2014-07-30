# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0010_computer_lastgrabbed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='computer',
            options={'ordering': [b'computerName', b'lanschoolName', b'serialNumber']},
        ),
        migrations.RenameField(
            model_name='computer',
            old_name='enrolledBy',
            new_name='enrollmentSet',
        ),
    ]
