from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework.urlpatterns import format_suffix_patterns
from .views import register, achievements, stats, Profile, friends_ranking, FriendRequests, requesting_me

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('register/', register, name="register"),
    path('profiles/<int:user_id>', Profile.as_view(), name="profile_detail"),
    path('profiles/', Profile.as_view(), name="profile"),
    path('stats/<int:user_id>', stats, name="stats"),
    path('achievements/<int:user_id>', achievements, name="user_achievements"),
    path('friends_ranking/<int:user_id>', friends_ranking, name="friends_ranking"),
    path('friend_requests/<username>', FriendRequests.as_view(), name="friend_requests"),
    path('friend_requests/requesting_me/<username>', requesting_me, name="friend_requests_requesting_me")
]

# This step is needed if using APIview classes
urlpatterns = format_suffix_patterns(urlpatterns)
