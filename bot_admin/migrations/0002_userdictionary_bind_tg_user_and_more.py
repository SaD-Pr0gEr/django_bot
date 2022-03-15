# Generated by Django 4.0.3 on 2022-03-15 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bot_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdictionary',
            name='bind_tg_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tg_user_dictionaries', to='bot_admin.telegramprofile', verbose_name='Привязанный telegram'),
        ),
        migrations.AlterField(
            model_name='userdictionary',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_dictionaries', to=settings.AUTH_USER_MODEL, verbose_name='Владелец словаря'),
        ),
    ]
