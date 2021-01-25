from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import register, edit, profile

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('register/', register, name="register"),
    path('edit/<int:user_id>', edit, name="edit_account"),
    path('profiles/<int:user_id>', profile, name="profile")
]
