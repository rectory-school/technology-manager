# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def delete_lanschool_users(apps, schema_editor):
	LanSchoolNameOption = apps.get_model("munkimanager", "LanSchoolNameOption")
	db = schema_editor.connection.alias
	
	LanSchoolNameOption.objects.using(db).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0003_auto_20140804_1901'),
    ]

    operations = [
		migrations.RunPython(delete_lanschool_users, ),
	
        migrations.AlterModelOptions(
            name='computer',
            options={'ordering': [b'computerName', b'description', b'serialNumber']},
        ),
        migrations.AddField(
            model_name='computer',
            name='studentID',
            field=models.CharField(default='', max_length=10, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lanschoolnameoption',
            name='boarder',
            field=models.BooleanField(default=False, verbose_name=b'Boarder/Day', choices=[(True, b'Boarding Student'), (False, b'Day Student')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lanschoolnameoption',
            name='grade',
            field=models.CharField(default=b'-', max_length=1, choices=[(b'-', b'Unknown/Other'), (b'K', b'Kindergarden'), (b'1', b'First Grade'), (b'2', b'Second Grade'), (b'3', b'Third Grade'), (b'4', b'Fourth Grade'), (b'5', b'Fifth Grade'), (b'6', b'Sixth Grade'), (b'7', b'Seventh Grade'), (b'8', b'Eigth Grade'), (b'9', b'Ninth Grade')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lanschoolnameoption',
            name='studentID',
            field=models.CharField(default='', unique=True, max_length=10),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='computer',
            name='lanschoolName',
        ),
    ]
