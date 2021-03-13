from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import contacts, donations

urlpatterns = [
    path('contacts/', contacts, name="contacts"),
    path('donations/', donations, name="donations"),
]

# This step is needed if using APIview classes
urlpatterns = format_suffix_patterns(urlpatterns)