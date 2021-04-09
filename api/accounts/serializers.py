from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import UserInformation, UserStats, UserAchievements, FriendRequest, Friends
 
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
        extra_kwargs = {'username': {'required': True}, 'email': {'required': True}, 'password': {'required': True}}   
 
class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        exclude = ['id']
        read_only_fields = ['email']

class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStats
        exclude = ['id']
        read_only_fields = ['email']

class UserAchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAchievements
        exclude = ['id']
        depth = 1

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        exclude = ['id']

class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        exclude = ['id']

