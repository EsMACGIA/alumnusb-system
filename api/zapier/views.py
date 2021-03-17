from accounts.models import UserStats, Donation, Contact
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import ContactSerializer, DonationSerializer, DonationUpdateSerializer
from django.db.models import Avg, Max, Min, Sum
from django.db.models.functions import TruncYear

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

def updateStatsOnDonations(contact_id):
    """
    Updates a given contact's stats based on his donations

    Parameters: 
    contact_id: id of the given contact

    """

    # Check if the contact exists
    try:
        contact = Contact.objects.get(id = contact_id)
    except Contact.DoesNotExist:
        return

    email = contact.email

    # Create default user stats if needed
    try:
        user_stat = UserStats.objects.get(email=email)
    except UserStats.DoesNotExist:
        user_stat = UserStats(email=email)

    # Get list of donations from the user 
    donations = Donation.objects.filter(contact_id=contact_id)
    
    # Calc new user_stat
    donations_data = donations.aggregate(Avg('amount'), Max('amount'), Min('amount'), Sum('amount'), Min('date'), Max('date'))

    user_stat.average_gift = donations_data['amount__avg']
    user_stat.largest_gift = donations_data['amount__max']
    user_stat.smallest_gift = donations_data['amount__min']
    user_stat.total_gifts = donations_data['amount__sum']

    best_year_aux = donations \
        .annotate(year=TruncYear('date')).values('year') \
        .annotate(total=Sum('amount'))
    best_year_total = best_year_aux.aggregate(Max('total'))['total__max']

    user_stat.best_gift_year_total = best_year_total
    user_stat.best_gift_year = best_year_aux.get(total=best_year_total)['year'].year

    user_stat.first_gift_date = donations_data['date__min']
    user_stat.last_gift_date = donations_data['date__max']
    user_stat.total_number_of_gifts = donations.count()

    user_stat.save()

    return


@authentication_classes([])
@permission_classes([])
class DonationAPI(APIView):

    """
    Edit donation, create donation.
    """

    @authentication_classes([])
    @permission_classes([])
    def post(self, request):
        """ 
        Allow to create donations from zapier. 
        
        Parameters: 
        request : POST request with donation basic data (id, amount, contact_id, date)

        Returns: 
        Json with created donations's data
    
        """

        # Get the contact data from JSON to a python dictionary
        donation = JSONParser().parse(request)
        donation_serializer = DonationSerializer(data=donation)

        # Check if the body of the request was correct
        if not donation_serializer.is_valid():
            return JsonResponse(donation_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        # Save donation
        donation_serializer.save()

        # Update user stats based on the donation
        updateStatsOnDonations(contact_id=donation_serializer.data["contact"]["id"])

        return JsonResponse(donation, status=status.HTTP_201_CREATED)

    @authentication_classes([])
    @permission_classes([])
    def put(self, request, donation_id):  
        """ 
        Allow to update donations
        
        Parameters: 
        request : PUT request with donation basic data ( amount, contact_id, date)

        Returns: 
        Json with created donations's data
    
        """

        # Get the editform's content from JSON to a python dictionary
        donationJSON = JSONParser().parse(request)

        try:
            donation =  Donation.objects.get(id=donation_id)
        except Donation.DoesNotExist:
            return JsonResponse("The given donation does not exist", status=status.HTTP_404_NOT_FOUND)

        donation_serial = DonationUpdateSerializer(donation, data = donationJSON, partial=True)

        # Check for errors in the form 
        if not donation_serial.is_valid():
            return JsonResponse(donation_serial.errors, status=status.HTTP_400_BAD_REQUEST)

        donation_serial.save()

        # Update user stats based on the donation
        updateStatsOnDonations(contact_id=donation.contact.id)

        return JsonResponse(donation_serial.data, status=status.HTTP_200_OK)