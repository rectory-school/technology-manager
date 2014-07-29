from django.core.management.base import BaseCommand, CommandError
from munkimanager.models import Installable, Catalog

from distutils.version import LooseVersion, StrictVersion

import plistlib

class Command(BaseCommand):
	args = '<munki_all_catalog>'
	help = 'Imports the munki catalogs from the "all" file'

	def handle(self, *args, **options):
		if len(args) != 1:
			raise CommandError('Argument must be path to the all catalog')
		
		plistPath = args[0]
		
		try:
			f = open(plistPath, "rb")
		except IOError:
			raise CommandError('Could not open catalog file at %s' % plistPath)
			
		items = plistlib.readPlist(f)
		
		munkiInstallables = {}
		
		for item in items:
			name = item['name']
			version = LooseVersion(item['version'])
			displayName = item.get('display_name', name)
			catalogs = set(item.get('catalogs'))
			uninstallable = item.get('uninstallable', False)
			
			if name in munkiInstallables:
				if version > munkiInstallables[name]['version']:
					munkiInstallables[name]['version'] = version
					munkiInstallables[name]['displayName'] = displayName
					munkiInstallables[name]['uninstallable'] = uninstallable
			else:
				munkiInstallables[name] = {'version': version, 'displayName': displayName, 'uninstallable': uninstallable, 'catalogs': set()}
				
			munkiInstallables[name]['catalogs'] |= catalogs
		
		catalogs = {}
		for catalog in Catalog.objects.all():
			if not catalog.name in catalogs:
				catalogs[catalog.name] = catalog
		
		dbInstallables = {}
		for o in Installable.objects.all():
			dbInstallables[o.name] = o
		
		dbMissing = set(munkiInstallables.keys()) - set(dbInstallables.keys())
		dbExtra = set(dbInstallables.keys()) - set(munkiInstallables.keys())
		matched = set(dbInstallables.keys()) & set(munkiInstallables.keys())
		
		for name in dbMissing:
			displayName = munkiInstallables[name]['displayName']
			uninstallable = munkiInstallables[name]['uninstallable']
			packageCatalogs = munkiInstallables[name]['catalogs']
			
			installable = Installable(name=name, displayName=displayName, uninstallable=uninstallable)
			installable.save()
			
			for catalogName in packageCatalogs:
				if catalogName not in catalogs:
					catalog = Catalog(name=catalogName)
					catalog.save()
					catalogs[catalogName] = catalog
				else:
					catalog = catalogs[catalogName]
				
				installable.catalogs.add(catalog)
			
			installable.save()
		
		for name in dbExtra:
			o = dbInstallables[name]
			o.delete()
		
		for name in matched:
			displayName = munkiInstallables[name]['displayName']
			uninstallable = munkiInstallables[name]['uninstallable']
			packageCatalogs = munkiInstallables[name]['catalogs']
			
			changed = False
			
			dbInstallable = dbInstallables[name]
			if displayName != dbInstallable.displayName:
				dbInstallable.displayName = displayName
				changed = True
			
			if uninstallable != dbInstallable.uninstallable:
				dbInstallable.uninstallable = uninstallable
				changed = True
			
			dbPackageCatalogs = set([o.name for o in dbInstallable.catalogs.all()])
			
			#Missing catalogs
			for catalogName in (packageCatalogs - dbPackageCatalogs):
				if catalogName not in catalogs:
					catalog = Catalog(name=catalogName)
					catalog.save()
					catalogs[catalogName] = catalog
				else:
					catalog = catalogs[catalogName]
					
				dbInstallable.catalogs.add(catalog)
				changed = True
			
			#Extra catalogs
			for catalogName in (dbPackageCatalogs - packageCatalogs):
				dbInstallable.catalogs.remove(catalogs[catalogName])
				changed = True
				
			if changed:
				print name
			