# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0004_auto_20140818_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lanschoolnameoption',
            name='boarder',
            field=models.BooleanField(default=False, choices=[(True, b'Boarding Student'), (False, b'Day Student')]),
        ),
        migrations.AlterField(
            model_name='lanschoolnameoption',
            name='grade',
            field=models.CharField(default=b'-', max_length=1, choices=[(b'-', b'Unknown/Other'), (b'K', b'Kindergarden'), (b'1', b'First Grade'), (b'2', b'Second Grade'), (b'3', b'Third Grade'), (b'4', b'Fourth Grade'), (b'5', b'Fifth Grade'), (b'6', b'Sixth Grade'), (b'7', b'Seventh Grade'), (b'8', b'Eigth Grade'), (b'9', b'Ninth Grade')]),
        ),
    ]
