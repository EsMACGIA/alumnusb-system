from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework.urlpatterns import format_suffix_patterns
from .views import register, Profile

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('register/', register, name="register"),
    path('profiles/<int:user_id>', Profile.as_view(), name="profile_detail"),
    path('profiles/', Profile.as_view(), name="profile")
]

# This step is needed if using APIview classes
urlpatterns = format_suffix_patterns(urlpatterns)
