import csv, io, datetime
from django.shortcuts import render, redirect
from accounts.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404


@login_required
def profile_upload(request):
	if ( request.user.is_authenticated and request.user.is_staff):    
		template = "profile_upload.html"
		prompt = {
			'title': 'El orden del CSV deberia ser',
			'info': 'Account ID -> First Name -> Middle Name -> Last Name -> Mailing City -> Mailing State/Province -> USB Alumn -> Codigo AlumnUSB -> Mailing Country -> Email -> Mobile -> Cohorte -> Birthdate -> Age -> Undergrad Degree -> Graduate Degree -> Carnet -> USB Undergrad Campus -> Graduate Campus -> Work Email -> Workplace -> Donor -> Average Gift -> Largest Gift -> Smallest Gift -> Total Gifts -> Best Gift Year Total -> Best Gift Year -> Social Networks -> Twitter Account -> Instagram Account -> First Gift Date -> Last Gift Date -> Total Number of Gifts'
				  }
	
		if request.method == "GET":
			return render(request, template, prompt)    
	
		csv_file = request.FILES['file']    
		
		if not csv_file.name.endswith('.csv'):
			return render(request, template, prompt)    

		data_set = csv_file.read().decode('UTF-8') 
		io_string = io.StringIO(data_set)
		next(io_string)
		for column in csv.reader(io_string, delimiter=',', quotechar="|"):
			if ( len(column) < 34 ):
				error = 'Formato incorrecto de CSV'
				return render(request, template, {'title':error})
			
			UserInformation.objects.filter(email=column[9]).delete()
			UserStats.objects.filter(email=column[9]).delete()
			
			created2 = UserInformation.objects.update_or_create(
			first_name=column[1],
			middle_name=column[2],
			last_name=column[3],
			mailing_city=column[4],
			mailing_state=column[5],
			usb_alumn=is_bool(column[6]),
			codigo_alumn_usb=column[7],
			email=column[9],
			mobile=column[10],
			cohorte=is_int(column[11]),
			birthdate=transform_date(column[12]),
			age=is_int(column[13]),
			graduate_degree=column[15],
			carnet=is_int(column[16]),
			graduate_campus=column[18],
			work_email=column[19],
			workplace=column[20],
			donor=is_bool(column[21]),
			social_networks=column[28],
			twitter_account=column[29],
			instagram_account=column[30]
			)

			created = UserStats.objects.update_or_create(
			email=column[9],
			average_gift=is_float(column[22]),
			largest_gift=is_float(column[23]),
			smallest_gift=is_float(column[24]),
			total_gifts=is_float(column[25]),
			best_gift_year_total=is_float(column[26]),
			best_gift_year=is_int(column[27]),
			first_gift_date=transform_date(column[31]),
			last_gift_date=transform_date(column[32]),
			total_number_of_gifts=is_int(column[33])
			)
		return render(request, template, {'title':"La carga fue exitosa"})
	else:
		return redirect('home')



## Functions to help the csv loader
def is_int(x):
	if (x==''):
		return 0
	return x

def is_float(x):
	if (x==''):
		return 0.0
	return x

def transform_date(x):
	if (x==''):
		return '2020-01-01'
	return datetime.datetime.strptime(x, '%m/%d/%Y').strftime('%Y-%m-%d')

def is_bool(x):
	if (x=='1'):
		return True
	else:
		return False
	
