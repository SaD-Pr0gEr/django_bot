from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class LoginForm(forms.Form):
    """Форма логина"""

    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(attrs={"class": "form-control", "id": "form2Example1"})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "form2Example2"})
    )


class SignUpForm(UserCreationForm):
    """Форма регистрации"""

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "form2Example2"})
    )
    password2 = forms.CharField(
        label="Пароль ещё раз",
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "form2Example3"})
    )

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "id": "form2Example1", "label": "Email*"})
        }
