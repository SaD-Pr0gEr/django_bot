from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import redirect
from translate import Translator

from translator.forms import TranslateWordForm
from translator.models import Languages


@login_required(login_url="accounts:login")
def translate(request: WSGIRequest):
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
        save_data.value = translate_
        save_data.save()
        json = {
            "status": "created",
            "status_code": 201,
            "translate": translate_
        }
        return JsonResponse(json, status=201)
    return JsonResponse({"data": "bad request", "status": 400}, status=400)


@login_required(login_url="accounts:login")
def delete_history(request: WSGIRequest):
    request.user.user_words.all().delete()
    messages.success(request, "История успешно удалена")
    return redirect("main:home")


@login_required(login_url="accounts:login")
def delete_word(request: WSGIRequest, word_pk):
    check_word = request.user.user_words.filter(pk=word_pk).first()
    if not check_word:
        messages.info(request, "Слово не найдено")
        return redirect("main:home")
    check_word.delete()
    messages.success(request, "Успешно удалено")
    return redirect("main:home")
