from munkimanager.models import Computer

def computerManifest(computer):
	out = {}
	
	out['catalogs'] = set([catalog.name for catalog in computer.catalogs.all()])
	out['included_manifests'] = set([staticManifest.manifestName for staticManifest in computer.includedManifests.all()])
	out['managed_installs'] = set([item.name for item in computer.managedInstalls.all()])
	out['managed_uninstalls'] = set([item.name for item in computer.managedUninstalls.all()])
	out['optional_installs'] = set([item.name for item in computer.optionalInstalls.all()])
	
	if computer.enrollmentSet:
		out['catalogs'] |=  set([catalog.name for catalog in computer.enrollmentSet.catalogs.all()])
		out['included_manifests'] |= set([staticManifest.manifestName for staticManifest in computer.enrollmentSet.includedManifests.all()])
		out['managed_installs'] |= set([item.name for item in computer.enrollmentSet.managedInstalls.all()])
		out['managed_uninstalls'] |= set([item.name for item in computer.enrollmentSet.managedUninstalls.all()])
		out['optional_installs'] |= set([item.name for item in computer.enrollmentSet.optionalInstalls.all()])
	
	for key in out.keys():
		out[key] = list(out[key])
	
	return out

def staticManifest(staticManifest):
	out = {}
	
	out['catalogs'] = [catalog.name for catalog in staticManifest.catalogs.all()]
	out['included_manifests'] = [includedStaticManifest.manifestName for includedStaticManifest in staticManifest.includedManifests.all()]
	out['managed_installs'] = [item.name for item in staticManifest.managedInstalls.all()]
	out['managed_uninstalls'] = [item.name for item in staticManifest.managedUninstalls.all()]
	out['optional_installs'] = [item.name for item in staticManifest.optionalInstalls.all()]
	
	return out