from django.urls import path

from main.views import home

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
]
