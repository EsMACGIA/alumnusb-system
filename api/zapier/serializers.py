from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import Contact, Donation
  
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__' 

class DonationSerializer(serializers.ModelSerializer):

    contact_id = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(),source='contact', write_only=True)
    class Meta:
        model = Donation
        fields = ('id', 'contact_id', 'amount', 'date', 'contact')
        depth = 1



    
      