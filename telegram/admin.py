from django.contrib import admin

from telegram.models import TelegramProfile


@admin.register(TelegramProfile)
class TelegramProfileAdmin(admin.ModelAdmin):
    list_display = ['tg_user_ID', 'user']
    list_display_links = ['tg_user_ID']
    search_fields = ['tg_user_ID', 'user']
