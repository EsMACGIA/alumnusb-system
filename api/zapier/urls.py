from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import contacts, DonationAPI

urlpatterns = [
    path('contacts/', contacts, name="contacts"),
    path('donations/<donation_id>', DonationAPI.as_view(), name="donations_put"),
    path('donations/', DonationAPI.as_view(), name="donations"),
]

# This step is needed if using APIview classes
urlpatterns = format_suffix_patterns(urlpatterns)