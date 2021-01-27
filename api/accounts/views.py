from django.shortcuts import render
from accounts.models import User_information, User_stats, Profile_Picture, Achievements, User_Achievements
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import UserSerializer, UserInformationSerializer, UserStatsSerializer, UserAchievementsSerializer
from .utils import ErrorMessages, defaultUserStats, defaultUserInfo, AchievementsDic, AchievementsType
from datetime import date

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

@api_view(['GET'])
def achievements(request,user_id):

    """ 
    Administrates accounts achievements retrieving requests. 
    
    Parameters: 
    request : GET request 
    (int) user_id: requested user's id
    
    Returns: 
    Json with requested user's achievements
  
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
    achievs = Achievements.objects.all()
    user_achievs = []

    # When this loop is done user_achievs will have a list of jsons where the Date
    # will be None if the user doesn't have the given achievemnt
    for ach_model in achievs:
        ach_name = ach_model.Name
        ach = AchievementsDic[ach_name]
        n = None
        ach_date = None

        # If the user has the achievement 
        if User_Achievements.objects.filter(Owner=user_id,Achievement=ach_name).exists():
            ach_date = User_Achievements.objects.get(Owner=user_id,Achievement=ach_name).Date
        # If the achievement checks total number of donations
        elif ach.type == AchievementsType.TOTAL_NUMBER_OF_DONATIONS:
            n = user_stats.Total_number_of_gifts
        # If the achievement checks total sum of donations 
        elif ach.type == AchievementsType.TOTAL_SUM_DONATIONS:
            n = user_stats.Total_gifts
        # If the achievement checks the biggest donation
        elif ach.type == AchievementsType.LARGEST_DONATION:
            n = user_stats.Largest_gift
        # For the moment this case is reserved for 'Donante recurrente' achievement
        else:
            f = True
            n_gifts = user_stats.Total_number_of_gifts
            f = f if n_gifts != None else False 
            start = user_stats.Last_gift_date
            f = start if start != None else False
            last = date.today()
            
            months = ((last - start).days)//30
            f = False if months == 0 else f
 
            if(f and n_gifts/months >= 1):
                User_Achievements(Owner=user,Achievement=ach_model).save()
                new_ach = User_Achievements.objects.get(Owner=user_id,Achievement=ach_name)
                ach_date = new_ach.Date
        
        # If the achiev was based on total number or total sum or largest donation
        if n != None:
            if ( n is not None and n>=ach.goal ):
                User_Achievements(Owner=user,Achievement=ach_model).save()
                new_ach = User_Achievements.objects.get(Owner=user_id,Achievement=ach_name)
                ach_date = new_ach.Date

        user_achievs.append({"Date": ach_date, "Achievement": ach_name, "Description": ach_model.Description})
            
    return JsonResponse({"Achievements": user_achievs}, status=status.HTTP_200_OK)
        
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

