from accounts.models import UserStats
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import ContactSerializer

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def contacts(request):
    """ 
    Allow to create contacts from zapier. 
    
    Parameters: 
    request : POST request with contact basic data (id, email)

    Returns: 
    Json with created contact's data
  
    """

    # Get the contact data from JSON to a python dictionary
    contact = JSONParser().parse(request)
    contact_serializer = ContactSerializer(data=contact)

    # Check if the body of the request was correct
    if not contact_serializer.is_valid():
        return JsonResponse(contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    contact_serializer.save()

    return JsonResponse(contact, status=status.HTTP_201_CREATED) 