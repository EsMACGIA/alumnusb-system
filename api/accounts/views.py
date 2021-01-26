from django.shortcuts import render
from accounts.models import User_information, User_stats, Profile_Picture
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import UserSerializer, UserInformationSerializer, UserStatsSerializer
from .utils import ErrorMessages, defaultUserStats, defaultUserInfo

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
        user_stat = defaultUserStats(email)
        user_stat.save()

    # Add id to the form to show that the user was created
    form_content["id"] = user_serializer.data["id"]
    return JsonResponse(form_content, status=status.HTTP_201_CREATED) 

@api_view(['GET'])
def stats(request,user_id):
    """ 
    Administrates account stats retrieving requests. 
    
    Parameters: 
    request : GET request 
    (int) user_id: requested user's id
    
    Returns: 
    Json with requested user's stats
  
    """
    
    # User requested and requesting user must match
    if user_id != request.user.id:
        return JsonResponse(ErrorMessages.UnauthAccesAccount, status=status.HTTP_401_UNAUTHORIZED)

    # User must exist
    try:
        user =  User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse(ErrorMessages.UserNotFound, status=status.HTTP_404_NOT_FOUND)

    user_stats = User_stats.objects.get(Email=user.email)

    return JsonResponse(UserStatsSerializer(user_stats).data, status=status.HTTP_200_OK)

class Profile(APIView):

    """
    Edit profile, retrieve profile.
    """

    def get(self, request, user_id):
        """ 
        Administrates account's profile requests. 
        
        Parameters: 
        request : GET request 
        (int) user_id: requested user's id

        Returns: 
        Json with user's profile information
    
        """
        
        # User requested and requesting user must match
        if user_id != request.user.id:
            return JsonResponse(ErrorMessages.UnauthAccesAccount, status=status.HTTP_401_UNAUTHORIZED) 

        # User must exist
        try:
            user =  User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(ErrorMessages.UserNotFound, status=status.HTTP_404_NOT_FOUND)

        user_info = User_information.objects.get(Email=user.email)

        return JsonResponse(UserInformationSerializer(user_info).data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        """ 
        Administrates account edition requests. 
        
        Parameters: 
        request : PUT request with user User_information data except Picture, Email and Codigo_Alumn_USB
        (int) user_id: requested user's id

        Returns: 
        Json with updated user's information 
    
        """

        # Get the editform's content from JSON to a python dictionary
        form_content = JSONParser().parse(request)
        
        # User requested and requesting user must match
        if user_id != request.user.id:
            return JsonResponse(ErrorMessages.UnauthAccesAccount, status=status.HTTP_401_UNAUTHORIZED) 

        try:
            user =  User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(ErrorMessages.UserNotFound, status=status.HTTP_404_NOT_FOUND)

        user_info = User_information.objects.get(Email=user.email)
        user_info_serial = UserInformationSerializer(user_info, data = form_content, partial=True)

        # Check for errors in the form 
        if not user_info_serial.is_valid():
            return JsonResponse(user_info_serial.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_info_serial.save()

        return JsonResponse(user_info_serial.data, status=status.HTTP_200_OK)

