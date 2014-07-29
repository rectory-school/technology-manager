from django.contrib import admin
from munkimanager.models import StaticManifest, Computer, AutoLocalUser

class LocalUserInline(admin.TabularInline):
	model = AutoLocalUser

class ComputerAdmin(admin.ModelAdmin):
	filter_horizontal = ['managedInstalls', 'managedUninstalls', 'includedManifests', 'catalogs', 'optionalInstalls']
	
	inlines = [LocalUserInline]
	
class StaticManifestAdmin(admin.ModelAdmin):
	filter_horizontal = ['managedInstalls', 'managedUninstalls', 'includedManifests', 'catalogs', 'optionalInstalls']

admin.site.register(StaticManifest, StaticManifestAdmin)
admin.site.register(Computer, ComputerAdmin)