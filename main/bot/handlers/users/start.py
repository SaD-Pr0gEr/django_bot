import time

from django.contrib.auth import get_user_model
from telebot.types import Message, ReplyKeyboardRemove
from main.bot.archive.keyboards_archive import start_keyboards, dict_commands, language_keyboards, search_commands
from main.bot.archive.states_archive import start_commands_state, translate_commands_state, search_commands_state, \
    add_word_state
from main.bot.loader import bot
from telegram.models import TelegramProfile
from translator.models import WordsHistory, Dictionary


def start_reset(message: Message):
    start_commands_state.reset_state()
    start_commands_state.category = True
    bot.send_message(
        message.from_user.id,
        "Выберите команду",
        reply_markup=start_keyboards()
    )


@bot.message_handler(['start'])
def start(message: Message):
    if not TelegramProfile.objects.filter(tg_user_ID=message.from_user.id).first():
        TelegramProfile.objects.create(tg_user_ID=message.from_user.id)
    text = [
        "Привет! Я бот переводчик...",
        "Выбери команду",
    ]
    start_commands_state.category = True
    bot.send_message(
        message.from_user.id,
        "\n".join(text),
        reply_markup=start_keyboards()
    )


@bot.message_handler(func=lambda state: start_commands_state.category)
def get_category(message: Message):
    start_commands_state.category = None
    if message.text.lower() == "словари 📕":
        start_commands_state.dictionary = True
        text = [
            "Выберите команду для словарей"
        ]
        bot.send_message(
            message.from_user.id,
            "\n".join(text),
            reply_markup=dict_commands
        )
    elif message.text.lower() == "переводчик 🇬🇧":
        translate_commands_state.from_language = True
        text = [
            "Круто!",
            "C какого языка перевести?"
        ]
        bot.send_message(
            message.from_user.id,
            "\n".join(text),
            reply_markup=language_keyboards
        )
    elif message.text.lower() == "поиск слов 🔍":
        search_commands_state.search_type = True
        text = [
            "Окей... Выберите категорию поиска"
        ]
        bot.send_message(
            message.from_user.id,
            "\n".join(text),
            reply_markup=search_commands
        )
    elif message.text.lower() == "показать историю переводов 📓":
        text = [word.word for word in WordsHistory.objects.filter(
            tg_user__tg_user_ID=message.from_user.id
        ).all()]
        if text:
            bot.send_message(message.from_user.id, "История:")
            time.sleep(1)
            bot.send_message(message.from_user.id, "\n".join(text))
        else:
            bot.send_message("Вы ещё ничего не переводили)")
        start_reset(message)
    elif message.text.lower() == "добавить слово из истории в словарь ➕":
        add_word_state.get_dict = True
        get_dicts = [f"{dicts.pk} - {dicts.name}" for dicts in
                     Dictionary.objects.filter(tg_user__tg_user_ID=message.from_user.id).all()]
        if get_dicts:
            bot.send_message(
                message.from_user.id,
                "Вводите ID(номер) словаря",
                reply_markup=ReplyKeyboardRemove()
            )
            time.sleep(1)
            bot.send_message(message.from_user.id, "\n".join(get_dicts))
        else:
            bot.send_message(message.from_user.id, "Словарей нет")
    elif message.text.lower() == "синхронизировать с сайтом(история поиск, словари и тп)":
        user = get_user_model()
        check_user = user.objects.filter(user_profiles__tg_user_ID=message.from_user.id).first()
        if check_user:
            tg_user = TelegramProfile.objects.filter(tg_user_ID=message.from_user.id).first()
            get_user_words = WordsHistory.objects.filter(tg_user=tg_user).all()
            get_user_dict = Dictionary.objects.filter(tg_user=tg_user).all()
            if get_user_words:
                for data in get_user_words:
                    data.user = check_user
                    data.save()
            if get_user_dict:
                for save in get_user_dict:
                    save.user = check_user
                    save.save()
            get_site_user_words = WordsHistory.objects.filter(user=tg_user.user).all()
            if get_site_user_words:
                for word in get_site_user_words:
                    word.tg_user = tg_user
                    word.save()
            get_site_user_dicts = Dictionary.objects.filter(user=tg_user.user).all()
            if get_site_user_dicts:
                for dicts in get_site_user_dicts:
                    dicts.tg_user = tg_user
                    dicts.save()
            bot.send_message(message.from_user.id, "Уcпешно синхронизировано!")
        else:
            bot.send_message(message.from_user.id, "У вас нету аккаунтов на сайте!")
        start_reset(message)
    else:
        start_reset(message)
