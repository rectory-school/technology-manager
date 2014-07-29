from django.db import models

# Create your models here.
class Computer(models.Model):
	serialNumber = models.CharField(max_length=100, primary_key=True)
	lanschoolName = models.CharField(max_length=200, blank=True)
	description = models.CharField(max_length=400, blank=True)
	
class Installable(models.Model):
	name = models.CharField(max_length=400, primary_key=True)
	displayName = models.CharField(max_length=400, blank=True)
	uninstallable = models.BooleanField(default=False)
	
class StaticManifest(models.Model):
	manifestName = models.CharField(max_length=100, primary_key=True)
	description = models.CharField(max_length=200, blank=True)
	
	includedManifests = models.ManyToManyField('self', blank=True)
	managedInstalls = models.ManyToManyField(Installable, related_name='managed_installs')
	managedUninstalls = models.ManyToManyField(Installable, related_name='managed_uninstalls', limit_choices_to={'uninstallable': True})
	optionalInstalls = models.ManyToManyField(Installable, related_name='optional_installs')