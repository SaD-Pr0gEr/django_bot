from django.urls import path

from bot_admin.views import home, translate

app_name = 'main'

urlpatterns = [
    path("", home, name='home'),
    path("translate", translate, name='translate'),
]
