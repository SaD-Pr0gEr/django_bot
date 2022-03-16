from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from telegram.forms import TelegramProfileForm
from telegram.models import TelegramProfile
from translator.forms import TranslateWordForm, DictionaryForm, AddWordDictForm, AddNewWord
from translator.models import WordsHistory, Dictionary

User = get_user_model()


@login_required(login_url="accounts:login")
def home(request: WSGIRequest):
    search_query = request.GET.get("search")
    if search_query:
        all_words = WordsHistory.objects.filter(
            user=request.user,
            word__icontains=search_query
        ).select_related(
            "language",
            "to_language",
            "user"
        ).all()
    else:
        all_words = WordsHistory.objects.filter(user=request.user).select_related(
            "language",
            "to_language",
            "user"
        ).all()
    form = TelegramProfileForm()
    add_word_form = TranslateWordForm()
    add_dict_form = DictionaryForm()
    add_word_dict_form = AddWordDictForm()
    new_word_form = AddNewWord()
    add_word_dict_form.fields['word'].queryset = request.user.user_words.select_related("user").all()
    add_word_dict_form.fields['word'].label = "Слова из истории перевода"
    user_profiles = TelegramProfile.objects.filter(user=request.user).select_related("user").all()
    dicts_list = Dictionary.objects.filter(user=request.user).prefetch_related(
        "dictionary_words",
        "dictionary_words__word"
    ).all()
    context = {
        "title": "Главная страница",
        "user": request.user,
        "user_profiles": user_profiles,
        "add_tg_form": form,
        "all_words": all_words,
        "last_words": all_words[:5],
        "add_word_form": add_word_form,
        "dicts_list": dicts_list,
        "add_dict_form": add_dict_form,
        "add_word_dict_form": add_word_dict_form,
        "new_word_form": new_word_form
    }
    return render(
        request,
        "main/home.html",
        context=context
    )
