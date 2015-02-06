from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import datetime

from syncthingmanager.models import Folder, FolderPath, ManagedDevice, StubDevice

# Create your views here.
def stubDeviceData(request, id):
  stubDevice = StubDevice.objects.get(device_id=id)
  
  folders = stubDevice.folders.all()
  relevantFolderPaths = FolderPath.objects.filter(folders__in=folders).distinct()
  
  managedDevices = ManagedDevice.objects.filter(folderpath__in=relevantFolderPaths)
  stubDevices = StubDevice.objects.filter(folders__in=folders)
  
  allFolders = Folder.objects.all()
  
  data = {
    'devices': {},
    'folders': {},
    'allFolderIDs': []
  }
  
  for objectType in (managedDevices, stubDevices):
    for o in objectType:
      data['devices'][o.device_id] = {'updateConfigDict': o.updateConfigDict, 'newConfigDict': o.newConfigDict}
  
  for folder in folders:
    data['folders'][folder.name] = folder.updateConfigDict
  
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