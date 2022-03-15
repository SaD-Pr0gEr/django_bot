from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """менеджер для кастомного пользователя"""

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('email обязательный параметр')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """Кастомный пользователь"""

    email = models.EmailField(
        "email",
        unique=True,
    )
    password = models.CharField(_("Пароль"), max_length=120)
    date_joined = models.DateTimeField("Дата регистрации", auto_now_add=True)
    is_admin = models.BooleanField("Статус суперпользователя", default=False)
    is_staff = models.BooleanField("Статус персонала", default=False)
    is_active = models.BooleanField("Статус активности аккаунта", default=False)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email

    def __repr__(self):
        return f"Model CustomUser: {self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Список пользователей"
