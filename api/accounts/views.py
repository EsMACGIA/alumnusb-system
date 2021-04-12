from django.shortcuts import render
from accounts.models import UserInformation, UserStats, ProfilePicture, Achievements, UserAchievements, Friends, FriendRequest
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import UserSerializer, UserInformationSerializer, UserStatsSerializer, UserAchievementsSerializer, FriendRequestSerializer, FriendsSerializer
from .utils import ErrorMessages, defaultUserStats, defaultUserInfo, AchievementsDic, AchievementsType
from datetime import date
from rest_framework.exceptions import ValidationError
from itertools import chain

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
        raise ValidationError(user_serializer.errors)

    email = form_content['email']
    user_serializer.save()

    # Create user default information
    if not UserInformation.objects.filter(email=email).exists():
        user_info = defaultUserInfo(email)
        user_info.save()

    if not UserStats.objects.filter(email=email).exists():
        user_stat = defaultUserStats(email)
        user_stat.save()

    # Add id to the form to show that the user was created
    form_content["id"] = user_serializer.data["id"]
    return JsonResponse(form_content, status=status.HTTP_201_CREATED) 

def jwt_login_payload_handler(token, user=None, request=None):
    """ 
    Configures login endpoint to send aditional information aside a jwt token. 
    
    Parameters: 
    request : POST request with user basic data (password, username)
    (UserModel) user: User requested
    token: JWT token to be sent

    Returns: 
    Json with jwt token and requested user's id
  
    """
    payload = {
        'token': token,
        'user_id' : user.id,
        'is_admin' : user.is_superuser,
        'email' : user.email,
        'username' : user.username,
    }
    return payload

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

    user =  User.objects.get(pk=user_id)

    user_stats = UserStats.objects.get(email=user.email)

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

    user =  User.objects.get(pk=user_id)
    
    user_stats = UserStats.objects.get(email=user.email)
    achievs = Achievements.objects.all()
    user_achievs = []
    user_not_achievs = []

    # When this loop is done user_achievs will have a list of json achievements 
    # made by the user
    # On the other hand user_not_achievs will have a list of achievements not reached
    # by the user
    for ach_model in achievs:
        ach_name = ach_model.name
        ach_date = None
        ach = AchievementsDic[ach_name]
        n = -1
        
        # If the achievement checks total number of donations
        if ach.type == AchievementsType.TOTAL_NUMBER_OF_DONATIONS:
            n = user_stats.total_number_of_gifts
        # If the achievement checks total sum of donations 
        elif ach.type == AchievementsType.TOTAL_SUM_DONATIONS:
            n = user_stats.total_gifts
        # If the achievement checks the biggest donation
        elif ach.type == AchievementsType.LARGEST_DONATION:
            n = user_stats.largest_gift
        # For the moment this case is reserved for 'Donante recurrente' achievement
        else:
            f = True
            n_gifts = user_stats.total_number_of_gifts
            f = f if n_gifts else False 
            start = user_stats.last_gift_date
            f = f if start else False
            last = date.today()
            
            if start:
                months = ((last - start).days)//30
                # Edge case a month has not happened but there are gifts
                if months == 0:
                    n = 0
                    f = False
            else:
                f = False

            # In this case 0 is enough to achieve the goal because there is not a  
            # defined goal
            if(f and n_gifts/months >= 1):
                n = 0
        
        # Check if the achievement was already achieved
        try:
            old_ach = UserAchievements.objects.get(owner=user_id, achievement=ach_name)
        except:
            old_ach = None

        achieved = n>=ach.goal

        # If the user has the achievement and it is correct 
        if old_ach and achieved:
            ach_date = old_ach.date
        # If the user has the achievement and it is not correct 
        elif old_ach and not achieved:
            # Delete it
            old_ach.delete()

        
        # If chieved and did not exist before
        if achieved and not old_ach:
            # Create new achiev
            UserAchievements(owner=user,achievement=ach_model).save()
            new_ach = UserAchievements.objects.get(owner=user_id,achievement=ach_name)
            ach_date = new_ach.date
        
        if ach_date:
            user_achievs.append({"date": ach_date, "achievement": ach_name, "description": ach_model.description})
        else:
            user_not_achievs.append({"achievement": ach_name, "description": ach_model.description})
            
    return JsonResponse({"achieved": user_achievs, "not_achieved" : user_not_achievs}, status=status.HTTP_200_OK)
        
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

        user =  User.objects.get(pk=user_id)

        user_info = UserInformation.objects.get(email=user.email)

        return JsonResponse(UserInformationSerializer(user_info).data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        """ 
        Administrates account edition requests. 
        
        Parameters: 
        request : PUT request with user UserInformation data except Picture, Email and Codigo_Alumn_USB
        (int) user_id: requested user's id

        Returns: 
        Json with updated user's information 
    
        """

        # Get the editform's content from JSON to a python dictionary
        form_content = JSONParser().parse(request)
        
        # User requested and requesting user must match
        if user_id != request.user.id:
            return JsonResponse(ErrorMessages.UnauthAccesAccount, status=status.HTTP_401_UNAUTHORIZED) 

        user =  User.objects.get(pk=user_id)

        user_info = UserInformation.objects.get(email=user.email)
        user_info_serial = UserInformationSerializer(user_info, data = form_content, partial=True)

        # Check for errors in the form 
        if not user_info_serial.is_valid():
           raise ValidationError(user_info_serial.errors)
        
        user_info_serial.save()

        return JsonResponse(user_info_serial.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def friends_ranking(request,user_id):
    """ 
    Returns a list of friends andd total achievements of each of them of the requested user. 
    
    Parameters: 
    request : GET request 
    (int) user_id: requested user's id
    
    Returns: 
    Json with requested user's list of friends data
  
    """
    
    # User requested and requesting user must match
    if user_id != request.user.id:
        return JsonResponse(ErrorMessages.UnauthAccesAccount, status=status.HTTP_401_UNAUTHORIZED)

    user =  User.objects.get(pk=user_id)

    friends_a = Friends.objects.filter(friend_b_id=user_id).values()
    friends_b = Friends.objects.filter(friend_a_id=user_id).values()

    # List of friends id including the given user
    friends = list(chain(map(lambda x: x['friend_a_id'], friends_a), map(lambda x: x['friend_b_id'], friends_b), [user.id]))

    # Retrieve the needed data for each friend
    friends_rank = []
    for f in friends:
        f = User.objects.get(pk=f)
        total_achievements = UserAchievements.objects.filter(owner=f).count()
        total_donations = UserStats.objects.get(email=f.email).total_gifts
        friends_rank.append({'username': f.username,'total_achievements': total_achievements, 'total_donations': total_donations})
        
    return JsonResponse({'friends_ranking': friends_rank}, status=status.HTTP_200_OK)

@api_view(['POST'])
def accept_friend(request,username):
    """ 
    Returns a JSON with the data of the friends relation if created properly. 
    
    Parameters: 
    request : POST request with the usernames of both future friends
    username: username of the user that wants to accept the request
    
    Returns: 
    Json with information data of the friends relationship
  
    """

    user_a = request.user
    user_a_id = user_a.id
    
    # User requested and requesting user must match
    if username != user_a.username:
        return JsonResponse(ErrorMessages.UnauthAccesAccount, status=status.HTTP_401_UNAUTHORIZED)

    # Turn JSON into python dic
    form_content = JSONParser().parse(request)

    try:
        username_a = form_content["username_a"]
        username_b = form_content["username_b"]
    except:
        return JsonResponse({"error" : ["Wrong body."], "status_code": 400}, status=status.HTTP_400_BAD_REQUEST)

    # At least one of the involved friends must be the user using the endpoint
    if username_a != username and username_b != username:
        return JsonResponse(ErrorMessages.UnauthAccesAccount, status=status.HTTP_401_UNAUTHORIZED)


    # User_a will be the user using the endpoint
    if username_a != username:
        username_b, username_a = username_a, username_b

    # User b must exist
    try:
        user_b = User.objects.get(username=username_b)
        user_b_id = user_b.id
    except User.DoesNotExist:
        return JsonResponse(ErrorMessages.UserNotFound, status=status.HTTP_404_NOT_FOUND)

    # The friend request from user_b must exist else it would be an illegal 
    # operation 
    if not FriendRequest.objects.filter(requesting_id=user_b_id,requested_id=user_a_id).exists():
        return JsonResponse(ErrorMessages.UnauthAccesAccount, status=status.HTTP_401_UNAUTHORIZED)

    # Check if the given data is valid 
    error = {"error" : [], "status_code": 400}

    # Cannot add the same person twice
    if Friends.objects.filter(friend_a_id=user_a_id,friend_b_id=user_b_id).exists() or \
        Friends.objects.filter(friend_a_id=user_b_id,friend_b_id=user_a_id).exists():
        error["error"].append("The user to accept is already your friend.")

    # Cannot accept yourself
    if user_a_id == user_b_id:
        error["error"].append("Cannot be your own friend.")

    if len(error["error"]) > 0:
        return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)

    # Create the friends relationship 
    friends = Friends(friend_a=user_a, friend_b=user_b)
    friends.save()

    # Delete all the friend requests from both sides 
    FriendRequest.objects.filter(requesting_id=user_b_id,requested_id=user_a_id).delete()
    FriendRequest.objects.filter(requesting_id=user_a_id,requested_id=user_b_id).delete()

    return JsonResponse(FriendsSerializer(friends).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def requesting_me(request,username):
    """ 
    Returns a Json with a list of users that are requesting the given user_id. 
    
    Parameters: 
    request : GET request 
    username: username of the requested user
    
    Returns: 
    Json with list of users requesting the given user
  
    """
    
    # User requested and requesting user must match
    if username!= request.user.username:
        return JsonResponse(ErrorMessages.UnauthAccesAccount, status=status.HTTP_401_UNAUTHORIZED)

    # Get the requests and send only useful data
    requests = FriendRequest.objects.filter(requested_id=request.user.id)
    requesting_users = []
    for request in requests:
        user = {}
        user['request_date'] = request.date
        user['username'] = request.requesting.username
        user['user_id'] = request.requesting.id
        requesting_users.append(user)

    return JsonResponse({'requesting_users': requesting_users}, status=status.HTTP_200_OK)

class FriendRequests(APIView):

    """
    Retrieve, Reject, Accept, Create friend requests.
    """

    def get(self, request, username):
        """ 
        Retrieves account's friend requests. 
        
        Parameters: 
        request : GET request 
        username: requesting user's username

        Returns: 
        Json with user's friend requests
    
        """

        # User requested and requesting user must match
        if username != request.user.username:
            return JsonResponse(ErrorMessages.UnauthAccesAccount, status=status.HTTP_401_UNAUTHORIZED)

        # Get the requests and send only useful data
        requests = FriendRequest.objects.filter(requesting_id=request.user.id)
        requested_users = []
        for request in requests:
            user = {}
            user['request_date'] = request.date
            user['username'] = request.requested.username
            user['user_id'] = request.requested.id
            requested_users.append(user)

        return JsonResponse({'requested_users': requested_users}, status=status.HTTP_200_OK)

    def post(self, request, username):
        """ 
        Administrates request creation requests. 
        
        Parameters: 
        request : POST request 
        username: username of the user we want to request

        Returns: 
        Json with created request data
    
        """

        user_id = request.user.id
        user =  User.objects.get(pk=user_id)
        
        try:
            requested = User.objects.get(username=username)
            requested_id = requested.id
        except User.DoesNotExist:
            return JsonResponse({"error" : ["El usuario a agregar no se puede encontrar."], "status_code": 404}, status=status.HTTP_404_NOT_FOUND)

        # Check if the given data is valid 
        error = {"error" : [], "status_code": 400}

        # Cannot add the same person twice
        if FriendRequest.objects.filter(requesting_id=user_id,requested_id=requested_id).exists():
            error["error"].append("El usuario solicitado ya fue solicitado previamente.")

        # Cannot add a friend
        if Friends.objects.filter(friend_a_id=user_id, friend_b_id=requested_id).exists() \
            or Friends.objects.filter(friend_a_id=requested_id, friend_b_id=user_id).exists():
            error["error"].append("El usuario solicitado ya es tu amigo.")

        # Cannot invite yourself
        if user_id == requested_id:
            error["error"].append("No puedes ser tu propio amigo.")

        if len(error["error"]) > 0:
            return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)

        serial = FriendRequestSerializer(data={'requesting': user_id, 'requested': requested.id})

        # Check for errors in the serializer
        if not serial.is_valid():
            return JsonResponse(serial.errors, status=status.HTTP_400_BAD_REQUEST)

        serial.save()

        return JsonResponse(serial.data, status=status.HTTP_200_OK)

    def delete(self, request, username):
        """ 
        Reject account's friend request. 
        
        Parameters: 
        request : DELETE request 
        username: username we want to reject

        Returns: 
        Json with username of the deleted friend request

        """

        answer_json = {'user_rejected': username}

        # The rejected user must exist, if not then the request does not exist
        try:
            requesting_user = User.objects.get(username = username)
        except:
            return JsonResponse(answer_json, status=status.HTTP_200_OK)

        # If the friend request does not exist then it was deleted
        try:
            fr = FriendRequest.objects.get(requesting_id=requesting_user.id, requested_id=request.user.id)
        except:
            return JsonResponse(answer_json, status=status.HTTP_200_OK)

        fr.delete()
        return JsonResponse(answer_json, status=status.HTTP_200_OK)



