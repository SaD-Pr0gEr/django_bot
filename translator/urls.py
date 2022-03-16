from django.urls import path

from translator.views import translate, delete_history, delete_word, delete_dict, add_dict, add_word_dict, del_word_dict

app_name = 'translator'

urlpatterns = [
    path('translate/', translate, name='translate'),
    path('delete-history/', delete_history, name='delete_history'),
    path('delete-word/<int:word_pk>/', delete_word, name='delete_word'),
    path('del-dict/<int:dict_pk>', delete_dict, name='delete_dict'),
    path('add-dict/', add_dict, name='add_dict'),
    path('add-word-to-dict/', add_word_dict, name='add_word_dict'),
    path('del-word-from-dict/<int:dict_pk>/<int:word_pk>', del_word_dict, name='del_word_dict')
]
