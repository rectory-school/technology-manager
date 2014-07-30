from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
import pytz

from munkimanager.models import Computer, StaticManifest, AutoEnroll, LanSchoolNameOption

from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

from . import lib

import plistlib
import json

MAX_WEB_SELECTABLE_INSTALL_TIME = timedelta(days=1)

# Create your views here.
def manifest(request, manifestName):
	try:
		computer = Computer.objects.get(pk=manifestName)
		computer.lastGrabbed = datetime.now()
		computer.save()
		if not computer.enabled:
			return HttpResponseNotFound('Computer %s is disabled' % manifestName)
			
		manifestData = lib.computerManifest(computer)
			
	except Computer.DoesNotExist:
		try:
			staticManifest = StaticManifest.objects.get(pk=manifestName)
			manifestData = lib.staticManifest(staticManifest)
		except StaticManifest.DoesNotExist:
			return HttpResponseNotFound('Manifest %s not found' % manifestName)
	
			
	return HttpResponse(plistlib.writePlistToString(manifestData), content_type="text/plain")
	
def computerInfo(request, serialNumber):
	try:
		computer = Computer.objects.get(pk=serialNumber)
	except Computer.DoesNotExist:
		return HttpResponseNotFound('Computer with serial number "%s" does not exist' % serialNumber)
	
	if not computer.enabled:
		return HttpResponseNotFound('Computer %s is disabled' % manifestName)
	
	data = {'localUsers': []}
	
 	for key in ('serialNumber', 'lanschoolName', 'computerName', 'disabled'):
		value = getattr(computer, key, None)
		if value:
			data[key] = value
	
	for localUser in computer.autolocaluser_set.all():
		data['localUsers'].append({'Full Name': localUser.fullName, 'Username': localUser.userName, 'admin': localUser.admin, 'expirePassword': localUser.forcePasswordReset})
	
	return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def autoEnroll(request):
	if request.method != 'POST':
		return HttpResponseNotAllowed(['POST'])
	
	serialNumber = request.POST.get("serialNumber", None)
	enrollmentSetName = request.POST.get("enrollmentSet", None)
	description = request.POST.get("description", None)
	
	if not serialNumber:
		return HttpResponseBadRequest("Serial number is required")
	
	if not enrollmentSetName:
		return HttpResponseBadRequest("Enrollment set is required")
	
	try:
		enrollmentSet = AutoEnroll.objects.get(pk=enrollmentSetName)
	except AutoEnroll.DoesNotExist:
		return HttpResponseNotFound("Enrollment set not found")
	
	if not enrollmentSet.enrollmentAllowed:
		return HttpResponseBadRequest("Enrollment set is not accepting new enrollments")
	
	try:
		computer = Computer.objects.get(pk=serialNumber)
	except Computer.DoesNotExist:
		computer = None
		
	if computer:
		return HttpResponseForbidden("Serial number already exists in database")
		
	computer = Computer(pk=serialNumber)
	computer.enabled = enrollmentSet.setEnabled
	computer.enrollmentSet = enrollmentSet
	computer.description = description or ""
	computer.save()
	
	return HttpResponse("OK", content_type="text/plain")
	
def enrollmentRequest(request, serialNumber):
	try:
		computer = Computer.objects.get(pk=serialNumber)
	except Computer.DoesNotExist:
		return HttpResponseNotFound('Computer with serial number "%s" does not exist' % serialNumber)
	
	if not computer.enrollmentSet:
		return HttpResponseBadRequest("Computer is not associated with an enrollment set. Please correct it from the admin panel.")
		
	if not computer.enrollmentSet.enrollmentAllowed:
		return HttpResponseBadRequest("Enrollment set is not accepting new enrollments")
	
	if request.method == 'POST':
		lanschoolName = request.POST.get("lanschoolName", None)
		computerName = request.POST.get("computerName", None)
		changed = False
		
		if computer.enrollmentSet.requireLanschool and not computer.lanschoolName and lanschoolName:
			computer.lanschoolName = lanschoolName
			changed = True
			
		if computer.enrollmentSet.requireComputerName and not computer.computerName and computerName:
			computer.computerName = computerName
			changed = True
		
		if changed:
			computer.save()
		
		return redirect(reverse("munki-data-request", args=[serialNumber]))
		
		
	data = {'serial': serialNumber, 'availableInstalls': []}
	
	if computer.enrollmentSet.requireLanschool and not computer.lanschoolName:
		data['requireLanSchoolName'] = True
		data['lanschoolChoices'] = LanSchoolNameOption.objects.all()
		
	if computer.enrollmentSet.requireComputerName and not computer.computerName:
		data['requireComputerName'] = True
	
	if (datetime.now(pytz.utc) - computer.addedAt) < MAX_WEB_SELECTABLE_INSTALL_TIME:
		selectableInstalls = set(list(computer.enrollmentSet.selectableInstalls.all()))
	
	alreadyInstalled = set(list(computer.managedInstalls.all()))
		
	data['availableInstalls'] = list(selectableInstalls - alreadyInstalled)
	
	return render(request, "munkimanager/datarequest.html", data)
	
def selectInstall(request, serialNumber):
	if request.method != 'POST':
		return HttpResponseNotAllowed(['POST'])
	
	try:
		computer = Computer.objects.get(pk=serialNumber)
	except Computer.DoesNotExist:
		return HttpResponseNotFound('Computer with serial number "%s" does not exist' % serialNumber)
	
	if not computer.enrollmentSet:
		return HttpResponseBadRequest("Computer is not associated with an enrollment set. Please correct it from the admin panel.")
		
	if not computer.enrollmentSet.enrollmentAllowed:
		return HttpResponseBadRequest("Enrollment set is not accepting new enrollments")
	
	if (datetime.now(pytz.utc) - computer.addedAt) < MAX_WEB_SELECTABLE_INSTALL_TIME:
		HttpResponseBadRequest("Maximum time to auto enroll in web installs has been exceeded")
	
	installName = request.POST.get("installName", None)
	if not installName:
		return HttpResponseBadRequest("Install name is required")
	
	installable = computer.enrollmentSet.selectableInstalls.get(pk=installName)
	computer.managedInstalls.add(installable)
	computer.save()
	
	return redirect(reverse("munki-data-request", args=[serialNumber]))
		
	