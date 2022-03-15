from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from dotenv import load_dotenv

from accounts.email_senders import confirm_email
from accounts.forms import LoginForm, SignUpForm

load_dotenv()

User = get_user_model()


def signup_page(request: WSGIRequest):
    if not request.user.is_anonymous:
        messages.info(request, "Вы уже вошли в систему")
        return redirect("main:home")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            email = user_data['email']
            check_email = User.objects.filter(email=email).first()
            if not check_email:
                password = user_data['password1']
                user = form.save(commit=False)
                user.set_password(password)
                domain = request.META['HTTP_HOST']
                confirm_url = f"{domain}{reverse('accounts:email_confirm', kwargs={'email': user.email})}"
                # confirm_email(user.email, confirm_url, domain)
                user.save()
                messages.success(request, 'Проверьте почту и активируйте аккаунт!')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Пользователь с таким email уже существует!')
    else:
        form = SignUpForm()
    context = {
        "title": "Регистрация",
        "signup_form": form
    }
    return render(
        request,
        "accounts/signup.html",
        context=context
    )


def login_page(request: WSGIRequest):
    if not request.user.is_anonymous:
        messages.info(request, "Вы уже вошли в систему")
        return redirect("main:home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            email = form_data['email']
            password = form_data['password']
            if User.objects.filter(email=email).first():
                auth_user = authenticate(request, email=email, password=password)
                if auth_user:
                    login(request, auth_user)
                    messages.success(request, "Вы успешно вошли")
                    return redirect("main:home")
                else:
                    messages.error(request, "Логин или пароль неправильные")
            else:
                messages.info(request, "Пользователя с таким email не существует")
    else:
        form = LoginForm()
    context = {
        "title": "Вход",
        "login_form": form
    }
    return render(
        request,
        "accounts/login.html",
        context=context
    )


def email_confirm(request: WSGIRequest, email: str):
    user = User.objects.filter(email=email, is_active=False).first()
    if user:
        user.is_active = True
        user.save()
        messages.success(request, "Вы подтвердили почту! Можно войти в аккаунт!")
        return redirect("accounts:login")
    messages.info(request, "Аккаунт уже активирован либо не существует")
    return redirect("main:home")


@login_required(login_url="accounts:login")
def logout_users(request: WSGIRequest):
    if request.method == "GET":
        logout(request)
        messages.success(request, "Вы успешно вышли с системы")
    else:
        messages.info(request, "Разрешён только GET метод")
    return redirect("main:home")
