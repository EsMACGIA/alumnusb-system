from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import User_information, User_stats, User_Achievements
 
class UserSerializer(serializers.ModelSerializer):

    # Needed to hash the password on creation
    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user

    # Needed to hash the password on update
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
    class Meta:
        model = User_information
        exclude = ['id']
        read_only_fields = ['Email']

class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_stats
        exclude = ['id']
        read_only_fields = ['Email']

class UserAchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Achievements
        exclude = ['id']
        depth = 1



    
      