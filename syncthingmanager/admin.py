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
  readonly_fields = ["missing_folders", "last_configured", "last_configure_result"]
  
  def get_changeform_initial_data(self, request):
    return {
      'deviceID': request.GET.get('deviceID'),
      'name': request.GET.get('name'),
      'folders': models.Folder.objects.filter(name__in=request.GET.getlist('folder'))
    }
    
class FolderAdmin(admin.ModelAdmin):
  fields = ['name', 'relative_path', 'folderPaths', 'stubDevices']
  readonly_fields = ('folderPaths', 'stubDevices')

  def folderPaths(self, o):
    return "\n".join(map(str, models.FolderPath.objects.filter(folders=o)))
    
  def stubDevices(self, o):
    return ", ".join(map(str, models.StubDevice.objects.filter(folders=o)))
  
  folderPaths.short_description = "Managed devices"
  stubDevices.short_description = "Client devices"
    
# Register your models here.
admin.site.register(models.ManagedDevice, ManagedDeviceAdmin)
admin.site.register(models.Folder, FolderAdmin)
admin.site.register(models.StubDevice, SubDeviceAdmin)