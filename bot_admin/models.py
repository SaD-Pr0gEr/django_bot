from django.conf import settings
from django.db import models
from django.urls import reverse_lazy


# DICT_LANGUAGE_CHOICES = [
#     ("RU", "Русский"),
#     ("EN", "Английский")
# ]


class Languages(models.Model):
    """Модель языка словаря"""

    language = models.CharField(
        "Язык",
        max_length=120,
        unique=True
    )
    slug = models.SlugField("URL", unique=True)

    def __str__(self):
        return self.language

    def __repr__(self):
        return f"Model Languages: {self.language}"

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Список языков"


class TelegramProfile(models.Model):
    """Модель профиля телеги"""

    username = models.CharField(
        "Имя пользователя(username)",
        max_length=1000,
        help_text="начинается с @",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_profiles",
        verbose_name="Владелец профиля"
    )

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username

    # def get_absolute_url(self):
    #     return f'{reverse_lazy("main:home")}?user={self.pk}'

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили в telegram"
        ordering = ["username", ]


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

    def __str__(self):
        return self.word

    def __repr__(self):
        return f"Model History: {self.word}"

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "История перевода слов"
        ordering = ['-pk', ]
