from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from main.bot.buttons.configure import conf_buttons
from main.bot.keybhoards.default.configure import ConfigureKeyboards
from translator.models import Languages


def start_keyboards():
    start_conf_buttons = [
        [KeyboardButton(text="Словари 📕", ), KeyboardButton(text="Переводчик 🇬🇧", )],
        [KeyboardButton(text="Поиск слов 🔍", ), KeyboardButton(text="Показать историю переводов 📓", )],
        [KeyboardButton(text="Добавить слово из истории в словарь ➕", ),
         KeyboardButton(text="Синхронизировать с сайтом(история поиск, словари и тп)")]
    ]
    start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for button in start_conf_buttons:
        start_keyboard.add(*button)
    return start_keyboard


language_keyboards = ConfigureKeyboards(conf_buttons(
    [data.language for data in Languages.objects.all()]),
    resize=True
)

dict_commands = ConfigureKeyboards(conf_buttons([
    "Список словарей",
    "Содержимое словаря",
    "Создать словарь",
    "Удалить словарь"
]), resize=True)

search_commands = ConfigureKeyboards(conf_buttons([
    "По первой букве",
    "По совпадению букв",
    "Строго по словам",
]), resize=True)
