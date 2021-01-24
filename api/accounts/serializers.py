from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import User_information, User_stats
 
class UserSerializer(serializers.ModelSerializer):

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user

    def update(self, *args, **kwargs):
        user = super().update(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user
 
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')   
 
class UserInformationSerializer(serializers.ModelSerializer):
    Picture = serializers.StringRelatedField(many=False)
 
    class Meta:
        model = User_information
        fields = ('First_name', 'Middle_name', 'Last_name', 'Mailing_city', 'Mailing_state', 'USB_alumn', 'Codigo_Alumn_USB',
        'Mailing_country', 'Email', 'Mobile', 'Cohorte', 'Birthdate', 'Age', 'Undergrad_degree', 'Graduate_degree', 
        'Carnet', 'USB_undergrad_campus', 'Graduate_campus', 'Work_email', 'Workplace', 'Donor', 'Social_networks', 'Twitter_account', 
        'Instagram_account', 'Picture')

    

class UserStatsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User_information
        fields = ('Email', 'Average_gift', 'Largest_gift', 'Smallest_gift', 'Total_gifts', 'Best_gift_year_total', 'Best_gift_year',
        'Best_gift_year', 'First_gift_date', 'Last_gift_date', 'Total_number_of_gifts')
    
      