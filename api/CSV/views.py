from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from accounts.models import UserInformation,UserStats
from rest_framework.permissions import IsAuthenticated,IsAdminUser
import csv, io, datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def upload_csv_file(request):
  """
  Upload CSV file for load donations information

  Parameters:
  request : POST request with CSV file

  Returns:
  Json with the result of operation
  """
  if 'file' not in request.FILES:
    return JsonResponse({'status': 400, 'error': 'El campo file es requerido'}, status=status.HTTP_400_BAD_REQUEST)
  
  csv_file = request.FILES['file']

  if not csv_file.name.endswith('.csv'):
    return JsonResponse({'status': 400, 'error': 'El formato del archivo no es .csv'}, status=status.HTTP_400_BAD_REQUEST)

  try:
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):

      if (len(column) != 34):
        error = 'Formato incorrecto de CSV'
        return JsonResponse({'status': 400, 'error': error}, status=status.HTTP_400_BAD_REQUEST)

      UserInformation.objects.filter(email=column[9]).delete()
      UserStats.objects.filter(email=column[9]).delete()

      UserInformation.objects.update_or_create(
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

      UserStats.objects.update_or_create(
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

    return JsonResponse({'status': 200, 'message': 'La carga fue exitosa'}, status=status.HTTP_200_OK)

  except: 
    return JsonResponse({'status': 400, 'message': 'El formato del archivo no es correcto'}, status=status.HTTP_400_BAD_REQUEST)

## Functions to help the csv loader
def is_int(x):
	return 0 if x == '' else x

def is_float(x):
	return 0.0 if x == '' else x

def transform_date(x):
  return '2020-01-01' if x == '' else datetime.datetime.strptime(x, '%m/%d/%Y').strftime('%Y-%m-%d')

def is_bool(x):
	return x == '1'
