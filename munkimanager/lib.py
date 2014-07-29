import plistlib

attrMap = {'catalogs': 'catalogs', 'managed_installs': 'managedInstalls', 'managed_uninstalls': 'managedUninstalls', 'optional_installs': 'optionalInstalls', 'included_manifests': 'includedManifests'}

def makeManifest(o):
	out = {}
	
	
	
	for manifestKey, attr in attrMap.items():
		manager = getattr(o, attr, None)
		
		if not manager:
			continue
			
		out[manifestKey] = [item.getName() for item in manager.all()]
		
	return plistlib.writePlistToString(out)