from django.conf import settings
from django.db import models

from django.urls import reverse_lazy


class Languages(models.Model):
    """Модель языка словаря"""

    language = models.CharField(
        "Язык",
        max_length=120,
        unique=True
    )
    code_for_translator = models.CharField("Сокращенный код языка", max_length=20)
    slug = models.SlugField("URL", unique=True)

    def __str__(self):
        return self.language

    def __repr__(self):
        return f"Model Languages: {self.language}"

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Список языков"


class WordsHistory(models.Model):
    """Модель историй"""

    word = models.CharField("Слово", max_length=120)
    value = models.CharField("Перевод", max_length=120)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_words",
        verbose_name="Владелец истории"
    )
    language = models.ForeignKey(
        Languages,
        on_delete=models.CASCADE,
        related_name="language_words",
        verbose_name="С языка",
    )
    to_language = models.ForeignKey(
        Languages,
        on_delete=models.CASCADE,
        related_name="language_words_2",
        verbose_name="На язык",
    )

    def delete_word(self):
        return reverse_lazy("translator:delete_word", kwargs={"word_pk": self.pk})

    def __str__(self):
        return self.word

    def __repr__(self):
        return f"Model History: {self.word}"

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "История перевода слов"
        ordering = ['-pk', ]


class Dictionary(models.Model):
    """Модель словаря"""

    name = models.CharField("Название", max_length=120)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_dictionaries",
        verbose_name="Владелец"
    )

    def del_dict(self):
        return reverse_lazy("translator:delete_dict", kwargs={"dict_pk": self.pk})

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Model Dictionary: {self.name}"

    class Meta:
        verbose_name = "Словарь"
        verbose_name_plural = "Список созданных словарей"
        ordering = ["-pk", ]


class DictionaryWords(models.Model):
    """М2М модель для словаря и слов"""

    dictionary = models.ForeignKey(
        Dictionary,
        on_delete=models.CASCADE,
        related_name="dictionary_words",
        verbose_name="Словарь"
    )
    word = models.ForeignKey(
        WordsHistory,
        on_delete=models.CASCADE,
        related_name="word_dictionaries",
        verbose_name="Слова"
    )

    def del_data(self):
        return reverse_lazy("translator:del_word_dict", kwargs={"dict_pk": self.dictionary.pk, "word_pk": self.word.pk})

    def __str__(self):
        return self.dictionary.name

    def __repr__(self):
        return f"Model m2m dictionary-books: {self.dictionary.name}"

    class Meta:
        verbose_name = "Заполненный словарь"
        verbose_name_plural = "Заполненные словари"
