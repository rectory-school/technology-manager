# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def delete_lanschool_users(apps, schema_editor):
	LanSchoolNameOption = apps.get_model("munkimanager", "LanSchoolNameOption")
	db = schema_editor.connection.alias
	
	LanSchoolNameOption.objects.using(db).all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0005_auto_20140818_1421'),
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
            name='studentID',
            field=models.CharField(unique=True, max_length=10),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='computer',
            name='lanschoolName',
        ),
        migrations.AlterField(
            model_name='lanschoolnameoption',
            name='boarder',
            field=models.BooleanField(default=False, verbose_name=b'Boarder/Day', choices=[(True, b'Boarding Student'), (False, b'Day Student')]),
        ),
    ]
