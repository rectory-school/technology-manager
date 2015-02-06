from django.shortcuts import render
from django.http import JsonResponse

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
      data['devices'][o.device_id] = o.updateConfigDict
  
  for folder in folders:
    data['folders'][folder.name] = folder.updateConfigDict
  
  data['allFolderIDs'] = [folder.name for folder in allFolders]
  
  return JsonResponse(data)