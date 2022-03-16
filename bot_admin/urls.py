from django.urls import path

from bot_admin.views import home

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
]
