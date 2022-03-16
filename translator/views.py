from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from translate import Translator

from translator.forms import TranslateWordForm, DictionaryForm, AddWordDictForm, AddNewWord
from translator.models import Languages, Dictionary, DictionaryWords, WordsHistory


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
def delete_word(request: WSGIRequest, word_pk: int):
    check_word = request.user.user_words.filter(pk=word_pk).first()
    if not check_word:
        messages.info(request, "Слово не найдено")
        return redirect("main:home")
    check_word.delete()
    messages.success(request, "Успешно удалено")
    return redirect("main:home")


@login_required(login_url="accounts:login")
def delete_dict(request: WSGIRequest, dict_pk: int):
    get_dict = get_object_or_404(
        Dictionary,
        pk=dict_pk,
        user=request.user
    )
    get_dict.delete()
    messages.success(request, "Успешно удалено")
    return redirect("main:home")


@login_required(login_url="accounts:login")
def add_dict(request: WSGIRequest):
    if request.method == "POST":
        form = DictionaryForm(request.POST)
        if form.is_valid():
            save = form.save(commit=False)
            save.user = request.user
            save.save()
            messages.success(request, "Словарь успешно добавлен")
        else:
            messages.error(request, "Форма не валидна")
        return redirect("main:home")
    messages.info(request, "Разрешен толкьо GET метод")
    return redirect("main:home")


@login_required(login_url="accounts:login")
def add_word_dict(request: WSGIRequest):
    if request.method == "POST":
        form = AddWordDictForm(request.POST)
        if form.is_valid():
            dict_pk = request.POST['dictionary']
            word = form.cleaned_data['word']
            check_word = get_object_or_404(
                WordsHistory,
                user=request.user,
                word=word
            )
            check_unique = DictionaryWords.objects.filter(
                word=check_word,
                dictionary__pk=dict_pk,
                dictionary__user=request.user
            ).first()
            if check_unique:
                messages.info(request, "Слово уже есть в словаре")
                return redirect("main:home")
            save = form.save(commit=False)
            dict_pk = get_object_or_404(
                Dictionary,
                pk=dict_pk,
                user=request.user
            )
            save.dictionary = dict_pk
            save.save()
            messages.success(request, "Успешно добавили")
        else:
            messages.error(request, "Данные не валидны")
    else:
        messages.info(request, "Разрешен только POST метод")
    return redirect("main:home")


@login_required(login_url="accounts:login")
def del_word_dict(request: WSGIRequest, dict_pk: int, word_pk: int):
    check = DictionaryWords.objects.filter(
        dictionary__pk=dict_pk,
        word__pk=word_pk,
        dictionary__user=request.user
    ).first()
    if not check:
        return HttpResponse(status=404)
    check.delete()
    messages.success(request, "Успешно удалили")
    return redirect("main:home")


@login_required(login_url="accounts:login")
def add_new_word(request: WSGIRequest):
    if request.method == "POST":
        form = AddNewWord(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word']
            dictionary = request.POST['dictionary']
            check_dict = get_object_or_404(Dictionary, pk=dictionary)
            create_word = WordsHistory.objects.create(
                word=word,
                value=Translator("en", "ru").translate(word),
                user=request.user,
                language=Languages.objects.filter(code_for_translator="en").first(),
                to_language=Languages.objects.filter(code_for_translator="ru").first(),
            )
            DictionaryWords.objects.create(dictionary=check_dict, word=create_word)
            messages.success(request, "Добавили успешно")
        else:
            messages.error(request, "Форма не валидна")
    else:
        messages.info(request, "Разрешен только POST метод")
    return redirect("main:home")
