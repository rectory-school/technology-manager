from django.contrib import admin
from munkimanager.models import StaticManifest, Computer, AutoLocalUser, AutoEnroll
from django.utils.html import format_html
import ago
from datetime import datetime
import pytz

class LocalUserInline(admin.TabularInline):
	model = AutoLocalUser

class ComputerAdmin(admin.ModelAdmin):
	filter_horizontal = ['managedInstalls', 'managedUninstalls', 'includedManifests', 'catalogs', 'optionalInstalls']
	
	inlines = [LocalUserInline]
	
	fieldsets = [
		(None, {'fields': ['serialNumber', 'computerName', 'lanschoolName']}),
		('Advanced Options', {'fields': ['enrolledBy', 'enabled']}),
		('Munki Configuration', {'classes': ('collapse',), 'fields': ['catalogs', 'includedManifests', 'managedInstalls', 'managedUninstalls', 'optionalInstalls']})
	]
	
	list_display=["__str__", 'enabled',  'lastSeen', 'displayIncludedManifests']
	
	def enable(self, request, queryset):
		queryset.update(enabled=True)
	
	def disable(self, request, queryset):
		queryset.update(enabled=False)
	
	def lastSeen(self, obj):
		return ago.human(datetime.now(pytz.utc) - obj.lastGrabbed, precision=1)
	
	lastSeen.short_description = "Manifest Last Downloaded"
	
	def displayIncludedManifests(self, obj):
		return format_html(u"<br />".join([m.manifestName for m in obj.includedManifests.all()]))
	
	displayIncludedManifests.short_description = "Included Manifests"
	list_filter = ['enabled', 'enrolledBy']
	
	enable.short_description = "Enable selected computers"
	disable.short_description = "Disable selected computers"
	
	actions = ['enable', 'disable']
class StaticManifestAdmin(admin.ModelAdmin):
	filter_horizontal = ['managedInstalls', 'managedUninstalls', 'includedManifests', 'catalogs', 'optionalInstalls']

class AutoEnrollAdmin(admin.ModelAdmin):
	filter_horizontal = ['managedInstalls', 'managedUninstalls', 'includedManifests', 'catalogs', 'optionalInstalls']
	

admin.site.register(StaticManifest, StaticManifestAdmin)
admin.site.register(Computer, ComputerAdmin)
admin.site.register(AutoEnroll, AutoEnrollAdmin)
