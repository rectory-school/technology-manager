from django.core.management.base import BaseCommand, CommandError
from munkimanager.models import StaticManifest, Catalog, Installable
from django.db import transaction

import plistlib

attrMap = {'managed_installs': 'managedInstalls', 'managed_uninstalls': 'managedUninstalls', 'optional_installs': 'optionalInstalls'}

class Command(BaseCommand):
	args = '<manifest_name> <manifest_file>'
	help = 'Imports a single munki manifest into the database'

	def handle(self, *args, **options):
		if len(args) != 2:
			raise CommandError('Arguments must be manifest name, manifest file')
		
		manifestPlist = plistlib.readPlist(args[1])
		
		with transaction.atomic():
			manifest = StaticManifest(manifestName=args[0])
			manifest.save()
		
			for manifestKey, attr in attrMap.items():
				for installableName in manifestPlist.get(manifestKey, []):
					try:
						installable = Installable.objects.get(pk=installableName)
						getattr(manifest, attr).add(installable)
						
					except Installable.DoesNotExist:
						raise CommandError('Installable "%s" does not exist' % installableName)
					
		
			for catalogName in manifestPlist.get('catalogs', []):
				try:
					catalog = Catalog.objects.get(pk=catalogName)
					manifest.catalogs.add(catalog)
					
				except Catalog.DoesNotExist:
					raise CommandError('Catalog "%s" does not exist' % catalogName)
				
			for includedManifestName in manifestPlist.get('included_manifests', []):
				try:
					includedManifest = StaticManifest.objects.get(pk=includedManifestName)
					manifest.includedManifests.add(includedManifest)
					
				except StaticManifest.DoesNotExist:
					raise CommandError('Included Manifest "%s" does not exist' % includedManifestName)
		
			manifest.save()