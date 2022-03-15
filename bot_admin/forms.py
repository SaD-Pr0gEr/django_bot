from django import forms

from bot_admin.models import TelegramProfile, WordsHistory


class TelegramProfileForm(forms.ModelForm):
    """Форма добавления профиля с сайта"""

    class Meta:
        model = TelegramProfile
        fields = ("username", )
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Начните с @"})
        }


class TranslateWordForm(forms.ModelForm):
    """Форма перевода"""

    class Meta:
        model = WordsHistory
        fields = ("word", "language", "to_language")
        widgets = {
            "word": forms.TextInput(attrs={
                "placeholder": "Слово",
                "class": "form-control",
                "id": "word"
            }),
            "language": forms.Select(attrs={"class": "form-select", "id": "language"}),
            "to_language": forms.Select(attrs={"class": "form-select", "id": "to_language"})
        }
