from django import forms

from telegram.models import TelegramProfile


class TelegramProfileForm(forms.ModelForm):
    """Форма добавления профиля с сайта"""

    class Meta:
        model = TelegramProfile
        fields = ("username", )
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Начните с @"})
        }
