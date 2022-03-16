from django.urls import path

from telegram.views import add_profile, delete_tg_profile

app_name = 'telegram_app'

urlpatterns = [
    path('add-profile/', add_profile, name='add_profile'),
    path('del-profile/<int:profile_id>', delete_tg_profile, name='del_profile'),
]
