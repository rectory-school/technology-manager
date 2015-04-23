from django.db import models
from adminsortable.models import Sortable
from adminsortable.fields import SortableForeignKey

class MasterIgnoreLine(Sortable):
  ignore_line = models.CharField(max_length=254)
  
  def __str__(self):
    return self.ignore_line

# Create your models here.
class ManagedDevice(models.Model):
  device_name = models.CharField(max_length=50)
  sync_address = models.CharField(max_length=50)
  gui_address = models.URLField(max_length=254)
  device_id = models.CharField(max_length=63, unique=True)
  api_key = models.CharField(max_length=32)
  
  @property
  def newConfigDict(self):
    return {
      'Addresses': [self.sync_address], 
      'CertName': '',
      'Compression': "metadata",
      'DeviceID': self.device_id,
      'Introducer': False,
      'Name': self.device_name,
    }
  
  @property
  def updateConfigDict(self):
    return {
      'Addresses': [self.sync_address], 
      'DeviceID': self.device_id,
      'Name': self.device_name,
    }
  
  def __str__(self):
    return self.device_name
  
class Folder(models.Model):
  name = models.CharField(max_length=50, unique=True)
  relative_path = models.CharField(max_length=100)
  
  class Meta:
    ordering = ('name', )
  
  @property
  def deviceIDs(self):
    managedDevices = ManagedDevice.objects.filter(folderpath__folders=self)
    stubDevices = StubDevice.objects.filter(folders=self)
    
    return set([device.device_id for device in managedDevices]) | set([device.device_id for device in stubDevices])
  
  @property
  def updateConfigDict(self):
    devices = [{'DeviceID': deviceID} for deviceID in self.deviceIDs]
    
    return {'ID': self.name, 'Devices': devices}
  
  
  def __str__(self):
    return self.name

class FolderIgnore(Sortable):
  class Meta(Sortable.Meta):
    pass
          
  folder = SortableForeignKey(Folder)
  ignore_line = models.CharField(max_length=254)
  
  def __str__(self):
    return self.ignore_line
    
class FolderPath(models.Model):
  device = models.ForeignKey(ManagedDevice)
  local_path = models.CharField(max_length=254)
  rescan_interval = models.IntegerField(default=60)
  
  folders = models.ManyToManyField(Folder, blank=True)
  
  def __str__(self):
    return "%s: %s" % (self.device.device_name, self.local_path)

class StubDevice(models.Model):
  device_id = models.CharField(max_length=63, unique=True)
  device_name = models.CharField(max_length=50)
  
  folders = models.ManyToManyField(Folder, blank=True)
  missing_folders = models.ManyToManyField(Folder, related_name='missing_on')
  
  last_configured = models.DateTimeField(blank=True, null=True)
  last_configure_result = models.IntegerField(blank=True, null=True)
  
  @property
  def newConfigDict(self):
    return {
      'Addresses': ['dynamic'], 
      'CertName': '',
      'Compression': "metadata",
      'DeviceID': self.device_id,
      'Introducer': False,
      'Name': self.device_name,
    }
  
  @property
  def updateConfigDict(self):
    return {
      'DeviceID': self.device_id,
      'Name': self.device_name,
      'Addresses': ['dynamic']
    }
  
  def __str__(self):
    return self.device_name
