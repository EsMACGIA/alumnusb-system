from django.urls import include, path

urlpatterns = [
    path('accounts/',include('api.accounts.urls')),
    path('csv/', include('api.CSV.urls'))
]
