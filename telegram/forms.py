from django import forms

from telegram.models import TelegramProfile


class TelegramProfileForm(forms.ModelForm):
    """Форма добавления профиля с сайта"""

    class Meta:
        model = TelegramProfile
        fields = ("tg_user_ID", )
        widgets = {
            "tg_user_ID": forms.TextInput(attrs={"placeholder": "Вводите свой ID"})
        }
