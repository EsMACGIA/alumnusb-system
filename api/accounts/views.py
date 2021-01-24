from django.shortcuts import render
from accounts.models import User_information, User_stats, Profile_Picture
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import UserSerializer

# Create your views here.

def defaultUserInfo(email):
    """ 
    Returns a default User_information model filled with default data and the given email. 
    
    Parameters: 
    email (string): email needed inside the default object

    Returns: 
    User_information: User_information model filled with default data and the given email
  
    """

    return User_information(First_name='',Middle_name='',
                    Last_name='',Mailing_city='',USB_alumn=0,
                    Codigo_Alumn_USB='',Mailing_country='',
                    Email=email,Mobile='',Cohorte=0,Birthdate='2020-1-1',
                    Age=1,Undergrad_degree='',Graduate_degree='',Carnet=0,
                    USB_undergrad_campus='',Graduate_campus='',Work_email='',
                    Workplace='',Donor=1,Social_networks='',Twitter_account='',
                    Instagram_account='')


def defaultUserStat(email):
    """ 
    Returns a default User_stat model filled with default data and the given email. 
    
    Parameters: 
    email (string): email needed inside the default object

    Returns: 
    User_stat: User_stat  model filled with default data and the given email
  
    """
    return User_stats(Email=email,Average_gift=0,
                    Largest_gift=0,Smallest_gift=0,Total_gifts=0,
                    Best_gift_year_total=0,Best_gift_year=0, First_gift_date='2020-1-1', Last_gift_date='2020-1-1', Total_number_of_gifts=0)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register(request):
    """ 
    Administrates registration requests. 
    
    Parameters: 
    request : POST request with user basic data (password, username, email)

    Returns: 
    Json with created user's data
  
    """
    
    # Get the registration form's content from JSON to a python dictionary
    form_content = JSONParser().parse(request)
    user_serializer = UserSerializer(data=form_content)

    # Check if the body of the request was correct
    if not user_serializer.is_valid():
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    email = form_content['email']
    user_serializer.save()

    # Create user default information
    if not User_information.objects.filter(Email=email).exists():
        user_info = defaultUserInfo(email)
        user_info.save()

    if not User_stats.objects.filter(Email=email).exists():
        user_stat = defaultUserStat(email)
        user_stat.save()

    # Add id to the form to show that the user was created
    form_content["id"] = user_serializer.data["id"]
    return JsonResponse(form_content, status=status.HTTP_201_CREATED) 