from django.contrib import admin

from translator.models import WordsHistory, Dictionary, DictionaryBooks, Languages


@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    list_display = ['language', 'slug']
    list_display_links = ['language', ]
    search_fields = ['language', ]


@admin.register(WordsHistory)
class WordsHistoryAdmin(admin.ModelAdmin):
    list_display = ['word', 'user', 'language']
    list_display_links = ['word', ]
    search_fields = ['word', ]


@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]
    list_display_links = ["name", ]
    search_fields = ["name", "user"]


@admin.register(DictionaryBooks)
class DictionaryBooksAdmin(admin.ModelAdmin):
    list_display = ["word", "dictionary"]
    list_display_links = ["word", ]
    search_fields = ["word", "dictionary"]
