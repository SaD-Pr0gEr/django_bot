from django.conf import settings
from django.db import models
from django.urls import reverse_lazy


class TelegramProfile(models.Model):
    """Модель профиля телеги"""

    tg_user_ID = models.PositiveIntegerField(
        "ID пользователя",
        unique=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="user_profiles",
        verbose_name="Владелец профиля",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.tg_user_ID}"

    def __repr__(self):
        return f"{self.tg_user_ID}"

    def delete_profile(self):
        return reverse_lazy('telegram_app:del_profile', kwargs={"profile_id": self.pk})

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили в telegram"
        ordering = ["tg_user_ID", ]
