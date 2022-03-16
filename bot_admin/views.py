from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from telegram.forms import TelegramProfileForm
from telegram.models import TelegramProfile
from translator.forms import TranslateWordForm
from translator.models import WordsHistory

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
    user_profiles = TelegramProfile.objects.filter(user=request.user).select_related("user").all()
    context = {
        "title": "Главная страница",
        "user": request.user,
        "user_profiles": user_profiles,
        "add_tg_form": form,
        "all_words": all_words,
        "last_words": all_words[:5],
        "add_word_form": add_word_form
    }
    return render(
        request,
        "main/home.html",
        context=context
    )
