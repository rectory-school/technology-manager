from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from datetime import datetime
from munkimanager.models import Computer, StaticManifest
from . import lib

import json

# Create your views here.
def manifest(request, manifestName):
	try:
		manifest = Computer.objects.get(pk=manifestName)
		manifest.lastGrabbed = datetime.now()
		manifest.save()
		if not manifest.enabled:
			return HttpResponseNotFound('Computer manifest %s is disabled' % manifestName)
			
	except Computer.DoesNotExist:
		try:
			manifest = StaticManifest.objects.get(pk=manifestName)
		except StaticManifest.DoesNotExist:
			return HttpResponseNotFound('Manifest %s not found' % manifestName)
			
	return HttpResponse(lib.makeManifest(manifest), content_type="text/plain")
	
def computerInfo(request, serialNumber):
	try:
		computer = Computer.objects.get(pk=serialNumber)
	except Computer.DoesNotExist:
		return HttpResponseNotFound('Computer with serial number "%s" does not exist' % serialNumber)
	
	data = {'localUsers': []}
	
 	for key in ('serialNumber', 'lanschoolName', 'computerName', 'disabled'):
		value = getattr(computer, key, None)
		if value:
			data[key] = value
	
	for localUser in computer.autolocaluser_set.all():
		data['localUsers'].append({'Full Name': localUser.fullName, 'Username': localUser.userName, 'admin': localUser.admin, 'expirePassword': localUser.forcePasswordReset})
	
	return HttpResponse(json.dumps(data), content_type="application/json")
