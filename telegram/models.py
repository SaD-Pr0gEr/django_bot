from django.conf import settings
from django.db import models
from django.urls import reverse_lazy


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

    def delete_profile(self):
        return reverse_lazy('telegram_app:del_profile', kwargs={"profile_id": self.pk})

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили в telegram"
        ordering = ["username", ]
