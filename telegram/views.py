from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
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
        return HttpResponse(status=405)
