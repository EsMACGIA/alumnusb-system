from django.urls import path
from .views import upload_csv_file

urlpatterns = [
    path('upload-csv/', upload_csv_file),
]