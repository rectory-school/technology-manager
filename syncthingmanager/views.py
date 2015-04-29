from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import Http404

import datetime

from ipware.ip import get_ip

from syncthingmanager.models import Folder, FolderPath, ManagedDevice, StubDevice, MasterIgnoreLine, StubDeviceConfigurationFail

# Create your views here.
def stubDeviceData(request, id):
  try:
    stubDevice = StubDevice.objects.get(device_id=id)
  except StubDevice.DoesNotExist:
    configFail = StubDeviceConfigurationFail()
    configFail.device_id = id
    configFail.ip = get_ip(request)
    configFail.save()
    
    raise Http404("Stub device ID does not exist")
  
  folders = stubDevice.folders.all()
  relevantFolderPaths = FolderPath.objects.filter(folders__in=folders).distinct()
  
  managedDevices = ManagedDevice.objects.filter(folderpath__in=relevantFolderPaths)
  stubDevices = StubDevice.objects.filter(folders__in=folders)
  
  allFolders = Folder.objects.all()
  
  data = {
    'devices': {},
    'folders': {},
    'allFolderIDs': [],
    'ignores': {}
  }
  
  for objectType in (managedDevices, stubDevices):
    for o in objectType:
      data['devices'][o.device_id] = {'updateConfigDict': o.updateConfigDict, 'newConfigDict': o.newConfigDict}
  
  for folder in folders:
    data['folders'][folder.name] = folder.updateConfigDict
    
    ignores = [o.ignore_line for o in MasterIgnoreLine.objects.all()]
    
    for folderIgnore in [o.ignore_line for o in folder.folderignore_set.all()]:
      if folderIgnore not in ignores:
        ignores.append(folderIgnore)
    
    data['ignores'][folder.name] = ignores
  
  data['allFolderIDs'] = [folder.name for folder in allFolders]
  
  return JsonResponse(data)

@csrf_exempt
@require_http_methods(["POST"])
def setStubStatus(request, id):
  missingFolderNames = request.POST.getlist('folderName')
  lastConfigureResult = request.POST.get('lastUpdateResult')
  
  missingFolders = Folder.objects.filter(name__in=missingFolderNames)
  stubDevice = StubDevice.objects.get(device_id=id)
  
  stubDevice.missing_folders = missingFolders
  stubDevice.last_configured = datetime.datetime.now()
  stubDevice.last_configure_result = lastConfigureResult
  
  stubDevice.save()
  
  return JsonResponse({'Result': 'OK'})