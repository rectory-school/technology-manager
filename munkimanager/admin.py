from django.contrib import admin
from munkimanager.models import StaticManifest, Computer

class ComputerAdmin(admin.ModelAdmin):
	filter_horizontal = ['managedInstalls', 'managedUninstalls', 'includedManifests', 'catalogs', 'optionalInstalls']

class StaticManifestAdmin(admin.ModelAdmin):
	filter_horizontal = ['managedInstalls', 'managedUninstalls', 'includedManifests', 'catalogs', 'optionalInstalls']

admin.site.register(StaticManifest, StaticManifestAdmin)
admin.site.register(Computer, ComputerAdmin)