from django.db import models

# Create your models here.
class ManagedDevice(models.Model):
  device_name = models.CharField(max_length=50)
  sync_address = models.CharField(max_length=50)
  gui_address = models.URLField(max_length=254)
  deviceID = models.CharField(max_length=63, unique=True)
  apiKey = models.CharField(max_length=32)
  
  def __str__(self):
    return self.device_name
  
class Folder(models.Model):
  name = models.CharField(max_length=50)
  relative_path = models.CharField(max_length=100)
  
  def __str__(self):
    return self.name

class FolderPath(models.Model):
  device = models.ForeignKey(ManagedDevice)
  local_path = models.CharField(max_length=254)
  
  folders = models.ManyToManyField(Folder, blank=True)
  
  def __str__(self):
    return "%s: %s" % (self.device.device_name, self.local_path)

class StubDevice(models.Model):
  deviceID = models.CharField(max_length=63, unique=True)
  name = models.CharField(max_length=50)
  
  folders = models.ManyToManyField(Folder, blank=True)
  
  def __str__(self):
    return self.name