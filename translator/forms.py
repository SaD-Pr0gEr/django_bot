from django import forms

from translator.models import WordsHistory, Dictionary, DictionaryWords


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


class DictionaryForm(forms.ModelForm):
    """Форма для создания словаря"""

    class Meta:
        model = Dictionary
        fields = ("name", )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"})
        }


class AddWordDictForm(forms.ModelForm):
    """Форма добавления слово в словарь"""

    class Meta:
        model = DictionaryWords
        fields = ("word", )
        widgets = {
            "word": forms.Select(
                attrs={"class": "form-select"},
            ),
        }
