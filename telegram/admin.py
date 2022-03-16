from django.contrib import admin

from telegram.models import TelegramProfile


@admin.register(TelegramProfile)
class TelegramProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'user']
    list_display_links = ['username']
    search_fields = ['username', 'user']
