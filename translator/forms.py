from django import forms

from translator.models import WordsHistory


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
