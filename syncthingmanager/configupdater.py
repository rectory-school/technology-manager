#!/usr/bin/python

import copy
import logging
import os

from syncthingmanager.models import Folder, StubDevice, ManagedDevice, FolderPath, MasterIgnoreLine

logger = logging.getLogger(__name__)

def pathsEqual(*paths):
  def normalizePath(p):
    return p.replace("\\", "/")
  
  return len(set(map(normalizePath, paths))) == 1

#Returns a dict of {'folder.name': ('folder-path', 'folder')}
def getRelevantFolders(device):
  folderPaths = device.folderpath_set.all()
  
  out = {}
  
  for folderPath in folderPaths:
    for folder in folderPath.folders.all():
      if folder.name in out:
        raise DuplicateFolderError(folder.name, device)
      
      out[folder.name] = (folderPath, folder)
  
  return out

#Returns all the devices that our original device needs to know about
def getRelevantDevices(device):
  #In the comments of this function, me = device passed in as a parameter
  
  #Folder paths and folders assigned to me
  myFolderPaths = device.folderpath_set.all()
  myFolders = Folder.objects.filter(folderpath__in=myFolderPaths).distinct()
  
  #All the folder paths that myFolders are assigned to, on both myself and other devices
  theirFolderPaths = FolderPath.objects.filter(folders__in=myFolders)
  
  #Managed devices and stub devices that I need to know about
  relevantManagedDevices=ManagedDevice.objects.filter(folderpath__in=theirFolderPaths).distinct()
  relevantStubDevices = StubDevice.objects.filter(folders__in=myFolders).distinct()
  
  out = {}
  for deviceSet in (relevantManagedDevices, relevantStubDevices):
    for relevantDevice in deviceSet:
      out[relevantDevice.device_id] = relevantDevice
  
  return out

def getExistingFoldersWithPositions(config):
  out = {}

  for i, configFolder in enumerate(config["folders"]):
    out[configFolder["id"]] = (i, configFolder)
  
  return out
  

def getExistingDevicesWithPositions(config):
  out = {}
  
  for i, configDevice in enumerate(config["devices"]):
    out[configDevice["deviceID"]] = (i, configDevice)
  
  return out
  
#Returns a new dict representing a ST config with the devices section updated. Returns false if there are no updates
def updateConfigDevices(device, originalConfig):
  
  #Will be returned as part of the tuple
  update = False
  
  updatedConfig = copy.deepcopy(originalConfig)
  
  existingDevices = getExistingDevicesWithPositions(updatedConfig)
  desiredDevices = getRelevantDevices(device)
  
  existingDeviceIDs = set(existingDevices.keys())
  desiredDeviceIDs = set(desiredDevices.keys())
  
  #The fixups we have to look at
  missingDeviceIDs = desiredDeviceIDs - existingDeviceIDs
  extraDeviceIDs = existingDeviceIDs - desiredDeviceIDs
  matchedDeviceIDs = desiredDeviceIDs & existingDeviceIDs
  
  #When working on a matched device, use the updateConfigDict. updateConfigDict 
  #has a smaller set of keys to it, so if things were adjusted server-side 
  #we don't overwrite them
  for deviceID in matchedDeviceIDs:
    position, deviceConfig = existingDevices[deviceID]
    desiredConfig = desiredDevices[deviceID].updateConfigDict
    
    #Compare each key individually
    for key in desiredConfig:
      #Only update the name if it's for my device
      if deviceID == device.device_id and key != 'name':
        continue
        
      if deviceConfig[key] != desiredConfig[key]:
        logger.info("Updating %s on %s from '%s' to '%s'" % (key, deviceID, deviceConfig[key], desiredConfig[key]))
        update = True
        updatedConfig["devices"][position][key] = desiredConfig[key]
  
  #Look at my extra devices, before we change any other positions. Iterate them backwards so that we don't
  #delete the wrong entries
  extraDevicePositions = sorted([existingDevices[deviceID][0] for deviceID in extraDeviceIDs], reverse=True)
  for devicePosition in extraDevicePositions:
    logger.info("Removing device %s" % (config["devices"][devicePosition]["deviceID"]))
    update = True
    del updatedConfig["devices"][devicePosition] 
  
  
  #Add the missing devices
  for deviceID in missingDeviceIDs:
    update = True
    deviceConfig = desiredDevices[deviceID].newConfigDict
    updatedConfig["devices"].append(deviceConfig)
    logger.info("Adding device %s" % deviceID)
  
  if update:
    return updatedConfig
  
  return False

def updateConfigFolders(device, originalConfig):
  update = False
  
  updatedConfig = copy.deepcopy(originalConfig)
  
  existingFolders = getExistingFoldersWithPositions(originalConfig)
  desiredFolders = getRelevantFolders(device)
  
  existingFolderNames = set(existingFolders.keys())
  desiredFolderNames = set(desiredFolders.keys())
  
  #The changes we now have to fix
  missingFolderNames = desiredFolderNames - existingFolderNames
  extraFolderNames = existingFolderNames - desiredFolderNames
  matchedFolderNames = desiredFolderNames & existingFolderNames
  
  #For a matched ID, we look at the devices, path and rescan interval
  for folderName in matchedFolderNames:
    folderPath, folder = desiredFolders[folderName]
    position, configFolder = existingFolders[folderName]
    
    logger.info("Processing %s" % folderName)
    
    #This is probably ineffecient and will generate like 8000 SQL queries. Right now I don't care.
    newDeviceIDs = folder.deviceIDs
    currentDeviceIDs = set([configFolderDevice["deviceID"] for configFolderDevice in configFolder["devices"]])
    
    if newDeviceIDs != currentDeviceIDs:
      logger.info("Replacing device IDs with {devices}".format(devices=", ".join(list(newDeviceIDs))))
      update = True
      updatedConfig["folders"][position]["devices"]=[{'deviceID': deviceID} for deviceID in newDeviceIDs]
    
    newPath = os.path.join(folderPath.local_path, folder.relative_path)
    oldPath = configFolder["path"]
    
    if not pathsEqual(newPath, oldPath):
      raise PathMoveError(folderName, device, oldPath, newPath)
    
    if not configFolder["rescanIntervalS"] == folderPath.rescan_interval:
      logger.info("Adjusting rescan interval for {folder} on {device} to {interval}".format(
        folder=folderName, device=device.device_name, interval=folderPath.rescan_interval))
      
      updatedConfig["folders"][position]["rescanIntervalS"] = folderPath.rescan_interval
      update = True
  
  extraFolderPositions = sorted([existingFolders[folderName][0] for folderName in extraFolderNames], reverse=True)
  for folderPosition in extraFolderPositions:
    logger.info("Removing folder %s" % (updatedConfig["folders"][folderPosition]["id"]))
    update = True
    del updatedConfig["folders"][folderPosition]
  
  
  for folderName in missingFolderNames:
    logger.info("Adding folder %s" % folderName)
    
    folderPath, folder = desiredFolders[folderName]
    
    deviceIDs = folder.deviceIDs
 
    folderDict = {
      'copiers': 1,
      'devices': [{'DeviceID': deviceID} for deviceID in deviceIDs],
      'hashers': 0,
      'id': folder.name,
      'ignorePerms': False,
      'invalid': '',
      'lenientMtimes': False,
      'path': os.path.join(folderPath.local_path, folder.relative_path),
      'pullers': 16,
      'readOnly': False,
      'rescanIntervalS': folderPath.rescan_interval,
      'versioning': {u'Params': {}, u'Type': u''}
    }
    
    updatedConfig["folders"].append(folderDict)
    update = True
  
  if update:
    return updatedConfig
  
  return False
  
class DuplicateFolderError(Exception):
  def __init__(self, folderName, managedDevice):
    super(DuplicateFolderError, self).__init__('A duplidate folder path for {name} on {device} was found'.format(name=folderName, device=managedDevice.device_name))
    
    self.folderName = folderName
    self.managedDevice = managedDevice

class PathMoveError(Exception):
  def __init__(self, folderName, managedDevice, oldPath, newPath):
    message = "{folder} is attempting move from {oldPath} to {newPath} on {device}".format(folder=folderName, oldPath=oldPath, newPath=newPath, device=managedDevice.device_name)
    
    super(PathMoveError, self).__init__(message)
    
    self.folderName = folderName
    self.managedDevice = managedDevice
    self.oldPath = oldPath
    self.newPath = newPath
    