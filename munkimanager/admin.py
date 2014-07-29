from django.contrib import admin
from munkimanager.models import StaticManifest, Computer, AutoLocalUser, AutoEnroll

class LocalUserInline(admin.TabularInline):
	model = AutoLocalUser

class ComputerAdmin(admin.ModelAdmin):
	filter_horizontal = ['managedInstalls', 'managedUninstalls', 'includedManifests', 'catalogs', 'optionalInstalls']
	
	inlines = [LocalUserInline]
	
	fieldsets = [
		(None, {'fields': ['serialNumber', 'computerName', 'lanschoolName']}),
		('Advanced Options', {'fields': ['enrolledBy', 'disabled']}),
		('Munki Data', {'classes': ('collapse',), 'fields': ['catalogs', 'includedManifests', 'managedInstalls', 'managedUninstalls', 'optionalInstalls']})
	]
class StaticManifestAdmin(admin.ModelAdmin):
	filter_horizontal = ['managedInstalls', 'managedUninstalls', 'includedManifests', 'catalogs', 'optionalInstalls']

class AutoEnrollAdmin(admin.ModelAdmin):
	filter_horizontal = ['managedInstalls', 'managedUninstalls', 'includedManifests', 'catalogs', 'optionalInstalls']
	

admin.site.register(StaticManifest, StaticManifestAdmin)
admin.site.register(Computer, ComputerAdmin)
admin.site.register(AutoEnroll, AutoEnrollAdmin)
