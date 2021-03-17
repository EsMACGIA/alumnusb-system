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

# This serializer is desgined to be used only when updating donations
class DonationUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Donation
        fields = ('id', 'contact_id', 'amount', 'date')
        read_only_fields = ['id', 'contact_id']
        depth = 1

    
      