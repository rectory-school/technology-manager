from django.core.management.base import BaseCommand, CommandError
from munkimanager.models import LanSchoolNameOption
from django.db import transaction
import xlrd

import requests

class Command(BaseCommand):
	args = 'csv_file'
	help = 'Imports the lanschool names. Fields should be labeled as LanSchool_User_Name, Grade_current and BoarderDay_current'

	def handle(self, *args, **options):
		if len(args) != 1:
			raise CommandError('Argument must be the path to the XLSX file')
		
		filePath = args[0]
		workbook = xlrd.open_workbook(filePath)
		sheet = workbook.sheet_by_name(workbook.sheet_names()[0])
		numRows = sheet.nrows
						
		LS_HEADER = None
		GRADE_HEADER = None
		BOARDERDAY_HEADER = None
		STUDENTID_HEADER = None
		
		headers = sheet.row(0)
		
		for i,h in enumerate(headers):
			value = sheet.cell_value(0, i)
			
			if "::" in value:
				tableName, fieldName = value.rsplit("::", 1)
			
				
			if fieldName.lower() in ('lanschool_user_name', ):
				LS_HEADER = i
			elif fieldName.lower() in ('grade_current', ):
				GRADE_HEADER = i
			elif fieldName.lower() in ('boarderday_current', ):
				BOARDERDAY_HEADER = i
			elif fieldName.lower() in ('idstudent', ):
				STUDENTID_HEADER = i
				
		if LS_HEADER == None:
			raise CommandError('LanSchool_User_Name was not found')
		if GRADE_HEADER == None:
			raise CommandError('Grade_current was not found')
		if BOARDERDAY_HEADER == None:
			raise CommandError('BoarderDay_current was not found')
		if STUDENTID_HEADER == None:
			raise CommandError("IDSTUDENT was not found")
			
		with transaction.atomic():
			LanSchoolNameOption.objects.all().delete()
			
			for i in range(1, numRows):
				lanschoolName = sheet.cell_value(i, LS_HEADER)
				grade = sheet.cell_value(i, GRADE_HEADER)
				boarderDay = sheet.cell_value(i, BOARDERDAY_HEADER)
				studentID = sheet.cell_value(i, STUDENTID_HEADER)
					
				if boarderDay == 'B':
					boarder = True
				else:
					boarder = False
				
			
				o = LanSchoolNameOption()
				o.lanschoolName = lanschoolName
				o.grade = str(grade)
				o.boarder = boarder
				o.studentID = studentID
				o.save()
				
				print o.lanschoolName