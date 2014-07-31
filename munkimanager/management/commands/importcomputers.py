from django.core.management.base import BaseCommand, CommandError
from munkimanager.models import StaticManifest, Catalog, Installable, Computer, AutoEnroll, AutoLocalUser
from django.db import transaction

import biplist

munkiMapKeys = {
	'catalogs': ('MUNKI_CATALOG', Catalog),
	'managedInstalls': ('MUNKI_MANAGED_INSTALL', Installable),
	'managedUninstalls': ('MUNKI_MANAGED_UNINSTALL', Installable),
	'optionalInstalls': ('MUNKI_OPTIONAL_INSTALL', Installable),
	'includedManifests': ('MUNKI_INCLUDED_MANIFEST', StaticManifest),
}

enrollmentSetMap = {'Faculty One to One Laptops': 'Faculty Laptops', 
'Learning Lab': 'Learning Lab', 
'Administrative Desktops': 'Office Desktops', 
'Administrative Computers': 'Office Desktops', 
'Administrative Laptops': 'Office Laptops',
'Library Desktops': 'Student Desktops',
'Elementary Computers': 'Elementary Computers'
}

def _parseComputerInfo(d):
	out = {}
	
	out['serial'] = d.get('dstudio-host-serial-number', None)
	out['computerName'] = d.get('cn', "")
	out['hostName'] = d.get('dstudio-hostname', "")
	out['group'] = d.get('dstudio-group', None)
	
	customProperties = {}
	
	if 'dstudio-custom-properties' in d:
		for property in d['dstudio-custom-properties']:
			key = property['dstudio-custom-property-key']
			value = property['dstudio-custom-property-value']
			
			if not key in customProperties:
				customProperties[key] = []
				
			customProperties[key].append(value)
	
	out['localUser'] = _extractUserName(customProperties)
	out['munkiMap'] = _extractMunkiMap(customProperties)
	
	return out

def _extractMunkiMap(customProperties):
	out = {}
	
	for computerAttr, (dsKey, objClass) in munkiMapKeys.items():
		if dsKey in customProperties:
			out[computerAttr] = (objClass, customProperties[dsKey])
	
	return out
		

def _extractUserName(customProperties):
	userAttrs = ('LOCAL_USER_NAME', 'LOCAL_USER_ACCOUNT', 'LOCAL_USER_ADMIN')
	
	for attr in userAttrs:
		if attr not in customProperties:
			return None
		if len(customProperties[attr]) != 1:
			return None
	
	fullName = customProperties['LOCAL_USER_NAME'][0]
	userName = customProperties['LOCAL_USER_ACCOUNT'][0]
	admin = (customProperties['LOCAL_USER_ADMIN'][0].lower() in ('yes', 'y')) and True or False
	return {'fullName': fullName, 'userName': userName, 'admin': admin}

class Command(BaseCommand):
	args = 'ds_computer_file'
	help = 'Imports the DeployStudio computer list'

	def handle(self, *args, **options):
		if len(args) != 1:
			raise CommandError('Argument must be a link to the binary plist file')
		
		plist = biplist.readPlist(args[0])
		computers = plist['computers']
		
		with transaction.atomic():
			for computer in computers.values():
				computerInfo = _parseComputerInfo(computer)
				
				if not computerInfo['serial']:
					continue
				
				if not (computerInfo['localUser'] or computerInfo['munkiMap']):
					continue
					
				computerObj = Computer()
				computerObj.serialNumber = computerInfo['serial']
				computerObj.computerName = computerInfo['computerName']
				
				if computerInfo['group'] in enrollmentSetMap:
					enrollmentSetName = enrollmentSetMap[computerInfo['group']]
					try:
						enrollmentSet = AutoEnroll.objects.get(pk=enrollmentSetName)
					except AutoEnroll.DoesNotExist:
						enrollmentSet = AutoEnroll()
						enrollmentSet.name = enrollmentSetName
						enrollmentSet.enrollmentAllowed = False
						enrollmentSet.setEnabled = False
						enrollmentSet.requireComputerName = False
						enrollmentSet.requireLanschool = False
						enrollmentSet.save()
					
					computerObj.enrollmentSet = enrollmentSet
				
				computerObj.save()
				
				if computerInfo['localUser']:
					localUser = AutoLocalUser()
					localUser.computer = computerObj
					localUser.fullName = computerInfo['localUser']['fullName']
					localUser.userName = computerInfo['localUser']['userName']
					localUser.admin = computerInfo['localUser']['admin']
					
					localUser.save()
				
				for attr, (objClass, objNames) in computerInfo['munkiMap'].items():
					objs = [objClass.objects.get(pk=name) for name in objNames]
					setattr(computerObj, attr, objs)
				
				computerObj.save()
				
