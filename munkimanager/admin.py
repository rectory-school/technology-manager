from django.contrib import admin
from munkimanager.models import StaticManifest, Computer, AutoLocalUser, AutoEnroll, LanSchoolNameOption
from django.utils.html import format_html
import ago
from datetime import datetime
import pytz
from django.core.urlresolvers import reverse

class LocalUserInline(admin.TabularInline):
	model = AutoLocalUser

class ComputerAdmin(admin.ModelAdmin):
	filter_horizontal = ['managedInstalls', 'managedUninstalls', 'includedManifests', 'catalogs', 'optionalInstalls']
	search_fields = ['serialNumber', 'computerName', 'lanschoolName']
	
	inlines = [LocalUserInline]
	
	fieldsets = [
		(None, {'fields': ['serialNumber', 'computerName', 'lanschoolName']}),
		('Advanced Options', {'fields': ['enrollmentSet', 'enabled', 'description']}),
		('Munki Configuration', {'classes': ('collapse',), 'fields': ['catalogs', 'includedManifests', 'managedInstalls', 'managedUninstalls', 'optionalInstalls']})
	]
	
	list_display=["__str__", 'enabled',  'lastSeen', 'enrollmentSet']
	
	def enable(self, request, queryset):
		queryset.update(enabled=True)
	
	def disable(self, request, queryset):
		queryset.update(enabled=False)
	
	def lastSeen(self, obj):
		if obj.lastGrabbed:
			return ago.human(datetime.now(pytz.utc) - obj.lastGrabbed, precision=1)
		return "Never"
	
	lastSeen.short_description = "Manifest Last Downloaded"
	lastSeen.admin_order_field = 'lastGrabbed'
	
	list_filter = ['enabled', 'enrollmentSet']
	
	enable.short_description = "Enable selected computers"
	disable.short_description = "Disable selected computers"
	
	actions = ['enable', 'disable']
	
	def view_on_site(self, obj):
		return reverse('munki-manifest', args=(obj.serialNumber, ))

class StaticManifestAdmin(admin.ModelAdmin):
	filter_horizontal = ['managedInstalls', 'managedUninstalls', 'includedManifests', 'catalogs', 'optionalInstalls']

class AutoEnrollAdmin(admin.ModelAdmin):
	filter_horizontal = ['managedInstalls', 'managedUninstalls', 'includedManifests', 'catalogs', 'optionalInstalls', 'selectableInstalls']
	

admin.site.register(StaticManifest, StaticManifestAdmin)
admin.site.register(Computer, ComputerAdmin)
admin.site.register(AutoEnroll, AutoEnrollAdmin)
admin.site.register(LanSchoolNameOption, admin.ModelAdmin)