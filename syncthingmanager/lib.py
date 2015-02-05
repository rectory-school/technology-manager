#!/usr/bin/pytho

import requests
import os
import copy
import json

from syncthingmanager.models import Folder, StubDevice, ManagedDevice, FolderPath

def pathsEqual(*paths):
  def normalizePath(p):
    return p.replace("\\", "/")
  
  return len(set(map(normalizePath, paths))) == 1

def getRequest(device, call, data=None):
  url = "%srest/%s" % (device.gui_address, call)
  headers = {'X-API-Key': device.api_key}
  
  if data != None:
    func = requests.post
  else:
    func = requests.get
  
  if data:  
    r = func(url, data=data, headers=headers, verify=False)
  else:
    r = func(url, headers=headers, verify=False)
  
  try:
    return r.json()
  except ValueError:
    return r.text
  
def getConfig(device):
  return getRequest(device, "config")

def updateConfig(device):
  config = getConfig(device)
  originalDevice = device
  
  folderPaths = device.folderpath_set.all()
  #All folders directly assigned to this device
  relevantFolders = Folder.objects.filter(folderpath__in=folderPaths).distinct()
  
  #All the remote folder paths for the directly assigned folders
  relevantFolderPaths = FolderPath.objects.filter(folders__in=relevantFolders)
  
  #All the devices that have at least one shared folder with this device
  relevantManagedDevices=ManagedDevice.objects.filter(folderpath__in=relevantFolderPaths).distinct()
  relevantStubDevices = StubDevice.objects.filter(folders__in=relevantFolders).distinct()
  
  devicesByID = {}
  devicePositionsByID = {}
  
  newDevicesByID = {}
  
  #Note the current devices and where they are, so I can delete them by position later
  for i, device in enumerate(config["Devices"]):
    devicesByID[device["DeviceID"]] = device
    devicePositionsByID[device["DeviceID"]] = i
  
  #All the devices we should have
  for deviceSet in (relevantManagedDevices, relevantStubDevices):
    for device in deviceSet:
      newDevicesByID[device.device_id] = device
  
  newDeviceIDs = set(newDevicesByID.keys())
  deviceIDs = set(devicesByID.keys())
  
  #The fixups we have to look at
  missingDeviceIDs = newDeviceIDs - deviceIDs
  extraDeviceIDs = deviceIDs - newDeviceIDs
  matchedDeviceIDs = newDeviceIDs & deviceIDs
  
  #If we will be uploading and restarting the server
  update = False
  
  #When working on a matched device, use the updateConfigDict. updateConfigDict 
  #has a smaller set of keys to it, so if things were adjusted server-side 
  #we don't overwrite them
  for deviceID in matchedDeviceIDs:
    originalConfig = devicesByID[deviceID]
    newConfig = newDevicesByID[deviceID].updateConfigDict
    
    configPosition = devicePositionsByID[deviceID]
    
    #Compare each key individually
    for key in newConfig:
      #Only update the name if it's for our own device
      if deviceID == originalDevice.device_id and key != 'Name':
        continue
        
      if originalConfig[key] != newConfig[key]:
        print "Updating %s on %s from '%s' to '%s'" % (key, deviceID, originalConfig[key], newConfig[key])
        update = True
        config["Devices"][configPosition][key] = newConfig[key]
  
  
  #Look at my extra devices, before we change any other positions. Iterate them backwards so that we don't
  #delete the wrong entries      
  extraDevicePositions = sorted([devicePositionsByID[deviceID] for deviceID in extraDeviceIDs], reverse=True)
  for devicePosition in extraDevicePositions:
    print "Removing device %s" % (config["Devices"][devicePosition]["DeviceID"])
    update = True
    del config["Devices"][devicePosition] 
  
  #Add the missing devices
  for deviceID in missingDeviceIDs:
    update = True
    config["Devices"].append(newDevicesByID[deviceID].newConfigDict)
    print "Adding device %s" % deviceID
  
  foldersByID = {}
  folderPositionsByID = {}
  
  newFoldersByID = {}
  
  for i, folder in enumerate(config["Folders"]):
    foldersByID[folder["ID"]] = folder
    folderPositionsByID[folder["ID"]] = i
  
  for folder in relevantFolders:
    newFoldersByID[folder.name] = folder
    
  folderIDs = set(foldersByID.keys())
  newFolderIDs = set(newFoldersByID.keys())
  
  #The changes we now have to fix
  missingFolderIDs = newFolderIDs - folderIDs
  extraFolderIDs = folderIDs - newFolderIDs
  matchedFolderIDs = folderIDs & newFolderIDs
  
  #For a matched ID, we look at the devices, path and rescan interval
  for folderID in matchedFolderIDs:
    #Get the folder path for this server. Will throw an exception if the folder was
    #added to more than one path on this server
    
    folderPath = FolderPath.objects.get(folders__name=folderID, device=originalDevice)
    
    print "Processing %s" % folderID
    #Where the folder is in the config list so we can reference it by position
    folderPosition = folderPositionsByID[folderID]
    
    originalConfig = foldersByID[folderID]
    folder = newFoldersByID[folderID]
    
    #This is probably ineffecient and will generate like 8000 SQL queries. Right now I don't care.
    managedDevices = ManagedDevice.objects.filter(folderpath__folders=folder)
    stubDevices = StubDevice.objects.filter(folders=folder)
    
    newDeviceIDs = set([device.device_id for device in managedDevices]) | set([device.device_id for device in stubDevices])
    currentDeviceIDs = set([device["DeviceID"] for device in originalConfig["Devices"]])
    
    if newDeviceIDs != currentDeviceIDs:
      print "Replacing device IDs"
      update = True
      config["Folders"][folderPosition]["Devices"]=[{'DeviceID': deviceID} for deviceID in newDeviceIDs]
    
    newPath = os.path.join(folderPath.local_path, folder.relative_path)
    oldPath = originalConfig["Path"]
    
    if not pathsEqual(newPath, oldPath):
      #TODO: Raise a red flag on this. We shouldn't be moving paths.
      print "Moving path"
      config["Folders"][folderPosition]["Path"] = newPath
      update = True
      
    if not originalConfig["RescanIntervalS"] == folderPath.rescan_interval:
      print "Adjusting rescan interval"
      config["Folders"][folderPosition]["RescanIntervalS"] = folderPath.rescan_interval
      update = True
    
  extraFolderPositions = sorted([folderPositionsByID[folderID] for folderID in extraFolderIDs], reverse=True)
  for folderPosition in extraFolderPositions:
    print "Removing folder %s" % (config["Folders"][folderPosition]["ID"])
    update = True
    del config["Folders"][folderPosition]
    
  for folderID in missingFolderIDs:
    print "Adding folder %s" % folderID
    
    folder = newFoldersByID[folderID]
    
    #This is probably ineffecient and will generate like 8000 SQL queries. Right now I don't care.
    managedDevices = ManagedDevice.objects.filter(folderpath__folders=folder)
    stubDevices = StubDevice.objects.filter(folders=folder)
    
    deviceIDs = set([device.device_id for device in managedDevices]) | set([device.device_id for device in stubDevices])
    
    folderDict = {
      'Copiers': 1,
      'Devices': [{'DeviceID': deviceID} for deviceID in deviceIDs],
      'Hashers': 0,
      'ID': folder.name,
      'IgnorePerms': False,
      'Invalid': '',
      'LenientMtimes': False,
      'Path': os.path.join(folderPath.local_path, folder.relative_path),
      'Pullers': 16,
      'ReadOnly': False,
      'RescanIntervalS': folderPath.rescan_interval,
      'Versioning': {u'Params': {}, u'Type': u''}
    }
    
    config["Folders"].append(folderDict)
    update = True
    
  if update:
    print "Updating and reloading config"
    print getRequest(originalDevice, "config", data=json.dumps(config))
    print getRequest(originalDevice, "restart", data={})
  
  