from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404, redirect

from telegram.forms import TelegramProfileForm
from telegram.models import TelegramProfile


@login_required(login_url="accounts:login")
def delete_tg_profile(request: WSGIRequest, profile_id):
    get_profile = get_object_or_404(
        TelegramProfile,
        pk=profile_id,
        user=request.user
    )
    get_profile.delete()
    messages.success(request, "Профиль успешно удалён")
    return redirect("main:home")


@login_required(login_url="accounts:login")
def add_profile(request):
    if request.method == "POST":
        form = TelegramProfileForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['tg_user_ID']
            if TelegramProfile.objects.filter(tg_user_ID=user_id).first():
                messages.info(request, "Этот профиль уже добавлен")
                return redirect("main:home")
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            messages.success(request, "Успешно добавлен")
            return redirect("main:home")
        messages.error(request, "Данные не валидны")
    else:
        messages.info(request, "Разрешен только POST метод")
    return redirect("main:home")
