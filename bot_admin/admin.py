from django.contrib import admin

from bot_admin.models import Languages, TelegramProfile, WordsHistory


@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    list_display = ['language', 'slug']
    list_display_links = ['language', ]
    search_fields = ['language', ]


@admin.register(TelegramProfile)
class TelegramProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'user']
    list_display_links = ['username']
    search_fields = ['username', 'user']


@admin.register(WordsHistory)
class WordsHistoryAdmin(admin.ModelAdmin):
    list_display = ['word', 'user', 'language']
    list_display_links = ['word', ]
    search_fields = ['word', ]
