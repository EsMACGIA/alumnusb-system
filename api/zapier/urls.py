from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import contacts

urlpatterns = [
    path('contacts/', contacts, name="contacts"),
]

# This step is needed if using APIview classes
urlpatterns = format_suffix_patterns(urlpatterns)