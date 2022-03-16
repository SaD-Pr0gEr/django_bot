from django.urls import path

from translator.views import translate, delete_history, delete_word

app_name = 'translator'

urlpatterns = [
    path('translate/', translate, name='translate'),
    path('delete-history/', delete_history, name='delete_history'),
    path('delete-word/<int:word_pk>/', delete_word, name='delete_word'),
]
