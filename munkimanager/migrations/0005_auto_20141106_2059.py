# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munkimanager', '0004_auto_20140818_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoenroll',
            name='includedManifests',
            field=models.ManyToManyField(related_name=b'AutoEnrollIncludedManifests', verbose_name=b'Included Manifests', to=b'munkimanager.StaticManifest', blank=True),
        ),
        migrations.AlterField(
            model_name='autoenroll',
            name='managedInstalls',
            field=models.ManyToManyField(related_name=b'AutoEnrollInstalls', verbose_name=b'Managed Installs', to=b'munkimanager.Installable', blank=True),
        ),
        migrations.AlterField(
            model_name='autoenroll',
            name='managedUninstalls',
            field=models.ManyToManyField(related_name=b'AutoEnrollUninstalls', verbose_name=b'Managed Uninstalls', to=b'munkimanager.Installable', blank=True),
        ),
        migrations.AlterField(
            model_name='autoenroll',
            name='optionalInstalls',
            field=models.ManyToManyField(related_name=b'AutoEnrollOptionalInstalls', verbose_name=b'Optional Installs', to=b'munkimanager.Installable', blank=True),
        ),
        migrations.AlterField(
            model_name='autoenroll',
            name='selectableInstalls',
            field=models.ManyToManyField(related_name=b'AutoEnrollSelectableInstalls', verbose_name=b'Web Selectable Installs', to=b'munkimanager.Installable', blank=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='includedManifests',
            field=models.ManyToManyField(related_name=b'includedInComputer', verbose_name=b'Included Manifests', to=b'munkimanager.StaticManifest', blank=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='managedInstalls',
            field=models.ManyToManyField(related_name=b'computerInstalls', verbose_name=b'Managed Installs', to=b'munkimanager.Installable', blank=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='managedUninstalls',
            field=models.ManyToManyField(related_name=b'computerUninstalls', verbose_name=b'Managed Uninstalls', to=b'munkimanager.Installable', blank=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='optionalInstalls',
            field=models.ManyToManyField(related_name=b'computerOptionalInstalls', verbose_name=b'Optional Installs', to=b'munkimanager.Installable', blank=True),
        ),
        migrations.AlterField(
            model_name='staticmanifest',
            name='catalogs',
            field=models.ManyToManyField(related_name=b'+', to=b'munkimanager.Catalog', blank=True),
        ),
        migrations.AlterField(
            model_name='staticmanifest',
            name='includedManifests',
            field=models.ManyToManyField(related_name=b'includedInStatic', verbose_name=b'Included Manifests', to=b'munkimanager.StaticManifest', blank=True),
        ),
        migrations.AlterField(
            model_name='staticmanifest',
            name='managedInstalls',
            field=models.ManyToManyField(related_name=b'staticInstalls', verbose_name=b'Managed Installs', to=b'munkimanager.Installable', blank=True),
        ),
        migrations.AlterField(
            model_name='staticmanifest',
            name='managedUninstalls',
            field=models.ManyToManyField(related_name=b'staticUninstalls', verbose_name=b'Managed Uninstalls', to=b'munkimanager.Installable', blank=True),
        ),
        migrations.AlterField(
            model_name='staticmanifest',
            name='optionalInstalls',
            field=models.ManyToManyField(related_name=b'staticOptionalInstalls', verbose_name=b'Optional Installs', to=b'munkimanager.Installable', blank=True),
        ),
    ]
