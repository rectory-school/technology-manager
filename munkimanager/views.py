from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from munkimanager.models import Computer, StaticManifest
from . import lib

# Create your views here.
def manifest(request, manifestName):
	try:
		manifest = Computer.objects.get(pk=manifestName)
		if manifest.disabled:
			return HttpResponseNotFound('Computer manifest %s is disabled' % manifestName)
			
	except Computer.DoesNotExist:
		try:
			manifest = StaticManifest.objects.get(pk=manifestName)
		except StaticManifest.DoesNotExist:
			return HttpResponseNotFound('Manifest %s not found' % manifestName)
			
	return HttpResponse(lib.makeManifest(manifest), content_type="text/plain")