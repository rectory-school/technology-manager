#!/usr/bin/pytho

import requests
import os
import copy
import json
import time
import logging

import django_rq

from requests.exceptions import SSLError

from syncthingmanager.models import Folder, StubDevice, ManagedDevice, FolderPath, MasterIgnoreLine
from syncthingmanager.configupdater import updateConfigDevices, updateConfigFolders, getRelevantFolders

logger = logging.getLogger(__name__)

def pingWait(device):
  #Wait for ping response  
  while True:
    try:
      req = getRequest(device, "system/ping")
      if req["ping"] == "pong":
        return
    except SSLError as e:
      #Nonrecoverable error
      raise
    except Exception as e:
      logger.debug("No ping response yet: %s" % e)
      time.sleep(1)

def getRequest(device, call, data=None):
  url = "%srest/%s" % (device.gui_address, call)
  headers = {'X-API-Key': device.api_key}
  
  if data != None:
    func = requests.post
  else:
    func = requests.get
  
  if data:  
    r = func(url, data=data, headers=headers)
  else:
    r = func(url, headers=headers)
  
  try:
    return r.json()
  except ValueError:
    return r.text
  
def getConfig(device):
  return getRequest(device, "system/config")

def getIgnores(device, folder):
  req = getRequest(device, "db/ignores?folder=%s" % folder)
  
  ignores = req["ignore"]

  if ignores:
    return ignores
    
  return []

def updateIgnores(device, folder):
  currentIgnores = getIgnores(device, folder)
  oFolder = Folder.objects.get(name=folder)
  
  newIgnores = [o.ignore_line for o in MasterIgnoreLine.objects.all()]
  
  for ignoreLine in [o.ignore_line for o in oFolder.folderignore_set.all()]:
    if not ignoreLine in newIgnores:
      newIgnores.append(ignoreLine)
  
  if currentIgnores != newIgnores:
    logger.info("Updating ignores for %s on %s" % (folder, device))
    
    data = {'ignore': list(newIgnores)}
  
    req = getRequest(device, "db/ignores?folder=%s" % folder, data=json.dumps(data))

def uploadConfig(device, config):
  pingWait(device)
  logger.debug(getRequest(device, "system/config", data=json.dumps(config)))
  pingWait(device)

def restart(device):
  pingWait(device)
  logger.debug(getRequest(device, "system/restart", data={}))
  pingWait(device)

def updateDevice(device):
  pingWait(device)
  
  config = getConfig(device)
  
  update = False
  
  deviceConfig = updateConfigDevices(device, config)
  if deviceConfig:
    config = deviceConfig
    update = True
  
  folderConfig = updateConfigFolders(device, config)
  if folderConfig:
    config = folderConfig
    update = True
  
  if update:
    uploadConfig(device, config)
    pingWait(device)
    restart(device)
    time.sleep(15)
  
  for folderPath, folder in getRelevantFolders(device).values():
    updateIgnores(device, folder)
