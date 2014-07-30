from django.db import models

class Catalog(models.Model):
	name = models.CharField(max_length=254, primary_key=True)
	
	class Meta:
		ordering = ['name']
	
	def getName(self):
		return self.name
	
	def __unicode__(self):
		return self.name
	
class Installable(models.Model):
	name = models.CharField(max_length=400, primary_key=True)
	displayName = models.CharField(max_length=400, blank=True)
	uninstallable = models.BooleanField(default=False)
	
	catalogs = models.ManyToManyField(Catalog)
	
	class Meta:
		ordering = ['name']
	
	def getName(self):
		return self.name
	
	def __unicode__(self):
		if self.displayName:
			return self.displayName
		return self.name
	
class StaticManifest(models.Model):
	manifestName = models.CharField(max_length=100, primary_key=True, verbose_name="Mainfest Name")
	description = models.CharField(max_length=200, blank=True)
		
	includedManifests = models.ManyToManyField('self', blank=True, related_name='includedInStatic', verbose_name="Included Manifests", symmetrical=False)
	managedInstalls = models.ManyToManyField(Installable, related_name='staticInstalls', blank=True, verbose_name="Managed Installs")
	managedUninstalls = models.ManyToManyField(Installable, related_name='staticUninstalls', limit_choices_to={'uninstallable': True}, blank=True, verbose_name="Managed Uninstalls")
	optionalInstalls = models.ManyToManyField(Installable, related_name='staticOptionalInstalls', blank=True, verbose_name="Optional Installs")
	
	catalogs = catalogs = models.ManyToManyField(Catalog, related_name='+')
	
	class Meta:
		ordering = ['manifestName']
	
	def getName(self):
		return self.manifestName
	
	def __unicode__(self):
		if self.description:
			return "%s (%s)" % (self.manifestName, self.description)
		return self.manifestName

class AutoEnroll(models.Model):
	name = models.CharField(max_length=100, verbose_name="Name", primary_key=True)
	
	catalogs = models.ManyToManyField(Catalog, blank=True)
	includedManifests = models.ManyToManyField(StaticManifest, blank=True, related_name='AutoEnrollIncludedManifests', verbose_name="Included Manifests")
	managedInstalls = models.ManyToManyField(Installable, related_name='AutoEnrollInstalls', blank=True, verbose_name="Managed Installs")
	managedUninstalls = models.ManyToManyField(Installable, related_name='AutoEnrollUninstalls', limit_choices_to={'uninstallable': True}, blank=True, verbose_name="Managed Uninstalls")
	optionalInstalls = models.ManyToManyField(Installable, related_name='AutoEnrollOptionalInstalls', blank=True, verbose_name="Optional Installs")
	
	selectableInstalls = models.ManyToManyField(Installable, related_name="AutoEnrollSelectableInstalls", blank=True, verbose_name="Web Selectable Installs")
	
	requireLanschool = models.BooleanField(default=False, verbose_name="Require LanSchool Name")
	requireComputerName = models.BooleanField(default=False, verbose_name="Require Computer Name")
	setEnabled = models.BooleanField(default=False, verbose_name="Enable on import")
	
	enrollmentAllowed = models.BooleanField(default=True, verbose_name="Allow web enrollment")
	
	class Meta:
		verbose_name="Enrollment Set"
		verbose_name_plural = "Enrollment Sets"
	
	def __unicode__(self):
		return self.name

class Computer(models.Model):
	serialNumber = models.CharField(max_length=100, primary_key=True, verbose_name="Serial Number")
	lanschoolName = models.CharField(max_length=200, blank=True, verbose_name="LanSchool Computer Name")
	computerName = models.CharField(max_length=50, blank=True, verbose_name="Computer Name")
	enrollmentSet = models.ForeignKey(AutoEnroll, blank=True, null=True, verbose_name="Enrollment Set")
	enabled = models.BooleanField(default=True)
	addedAt = models.DateTimeField(auto_now_add=True)
	lastGrabbed = models.DateTimeField(blank=True, null=True)
	
	def __unicode__(self):
		if self.computerName:
			return "%s (%s)" % (self.computerName, self.serialNumber)
		if self.lanschoolName:
			return "%s (%s)" % (self.lanschoolName, self.serialNumber)
		if self.description:
			return "%s (%s)" % (self.description, self.serialNumber)
		
		return self.serialNumber

	class Meta:
		ordering = ['computerName', 'lanschoolName', 'description', 'serialNumber']
	
	description = models.CharField(max_length=400, blank=True)

	catalogs = models.ManyToManyField(Catalog, blank=True)
	
	includedManifests = models.ManyToManyField(StaticManifest, blank=True, related_name='includedInComputer', verbose_name="Included Manifests")
	managedInstalls = models.ManyToManyField(Installable, related_name='computerInstalls', blank=True, verbose_name="Managed Installs")
	managedUninstalls = models.ManyToManyField(Installable, related_name='computerUninstalls', limit_choices_to={'uninstallable': True}, blank=True, verbose_name="Managed Uninstalls")
	optionalInstalls = models.ManyToManyField(Installable, related_name='computerOptionalInstalls', blank=True, verbose_name="Optional Installs")

class AutoLocalUser(models.Model):
	fullName = models.CharField(max_length=100, verbose_name="Full Name")
	userName = models.CharField(max_length=20, verbose_name="Username")
	admin = models.BooleanField(default=False, verbose_name="Admin")
	forcePasswordReset = models.BooleanField(default=False, verbose_name="Force Password Reset")
	computer = models.ForeignKey(Computer)
	
	def __unicode__(self):
		return "%s on %s" % (self.fullName, self.computer)

class LanSchoolNameOption(models.Model):
	lanschoolName = models.CharField(max_length=100, verbose_name="Lanschool Name")
	
	class Meta:
		ordering = ['lanschoolName']
	
	def __unicode__(self):
		return self.lanschoolName
	