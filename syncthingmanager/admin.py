from django.contrib import admin
from syncthingmanager import models

class FolderPathInline(admin.StackedInline):
  model = models.FolderPath
  filter_horizontal = ["folders"]
  
  extra = 0
  
class ManagedDeviceAdmin(admin.ModelAdmin):
  inlines = [FolderPathInline]

class SubDeviceAdmin(admin.ModelAdmin):
  filter_horizontal = ["folders"]
  
# Register your models here.
admin.site.register(models.ManagedDevice, ManagedDeviceAdmin)
admin.site.register(models.Folder)
admin.site.register(models.StubDevice, SubDeviceAdmin)