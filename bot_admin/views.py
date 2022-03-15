from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect
from translate import Translator

from bot_admin.forms import TelegramProfileForm, TranslateWordForm
from bot_admin.models import TelegramProfile, Languages

User = get_user_model()


@login_required(login_url="accounts:login")
def home(request: WSGIRequest):
    if request.method == "POST":
        form = TelegramProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if not username.startswith("@"):
                messages.info(request, "Профиль должен начаться с @")
                return redirect("main:home")
            if TelegramProfile.objects.filter(username=username).first():
                messages.info(request, "Этот профиль уже добавлен")
                return redirect("main:home")
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            messages.success(request, "Успешно добавлен")
            return redirect("main:home")
    else:
        form = TelegramProfileForm()
    add_word_form = TranslateWordForm()
    user = User.objects.filter(email=request.user.email).prefetch_related(
        "user_profiles",
        "user_words",
    ).first()
    all_words = user.user_words.select_related("language", "to_language").all()
    last_words = all_words[:5]
    context = {
        "title": "Главная страница",
        "user": user,
        "add_tg_form": form,
        "all_words": all_words,
        "last_words": last_words,
        "add_word_form": add_word_form
    }
    return render(
        request,
        "main/home.html",
        context=context
    )


@login_required(login_url="accounts:login")
def translate(request):
    if not request.method == "POST":
        return JsonResponse({"status": "method not allowed"}, status=405)
    form = TranslateWordForm(request.POST)
    if form.is_valid():
        from_lang = Languages.objects.filter(language=form.cleaned_data['language']).first()
        to_lang = Languages.objects.filter(language=form.cleaned_data['to_language']).first()
        translator = Translator(
            to_lang.code_for_translator.lower(),
            from_lang.code_for_translator.lower(),
        )
        translate_ = translator.translate(form.cleaned_data['word'])
        save_data = form.save(commit=False)
        save_data.user = request.user
        save_data.value = form.cleaned_data['word']
        save_data.save()
        json = {
            "status": "created",
            "status_code": 201,
            "translate": translate_
        }
        return JsonResponse(json, status=201)
    return JsonResponse({"data": "bad request", "status": 400}, status=400)
