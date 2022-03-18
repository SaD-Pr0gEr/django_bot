import time

from telebot.types import Message, ReplyKeyboardRemove

from main.bot.archive.states_archive import dict_commands_state, start_commands_state, add_word_state
from main.bot.buttons.configure import conf_buttons
from main.bot.handlers.users.start import start_reset
from main.bot.keybhoards.default.configure import ConfigureKeyboards
from main.bot.loader import bot
from telegram.models import TelegramProfile
from translator.models import Dictionary, WordsHistory, DictionaryWords


@bot.message_handler(func=lambda state: start_commands_state.dictionary)
def dict_manager(message: Message):
    start_commands_state.dictionary = None
    if message.text.lower() == "список словарей":
        data = [
            dictionary.name for dictionary in Dictionary.objects.filter(tg_user__tg_user_ID=message.from_user.id).all()
        ]
        if data:
            bot.send_message(message.from_user.id, "\n".join(data), reply_markup=ReplyKeyboardRemove())
        else:
            bot.send_message(message.from_user.id, "Словарей нет")
        start_reset(message)
    elif message.text.lower() == "содержимое словаря":
        dict_commands_state.dict_title = True
        check_dict = Dictionary.objects.filter(tg_user__tg_user_ID=message.from_user.id).all()
        if check_dict:
            bot.send_message(
                message.from_user.id,
                f"Выберайте словарь",
                reply_markup=ConfigureKeyboards(conf_buttons([
                    dict_data.name for dict_data in
                    check_dict
                ]),
                    resize=True
                )
            )
        else:
            dict_commands_state.reset_state()
            bot.send_message(message.from_user.id, "Словарей нет")
            start_reset(message)
    elif message.text.lower() == "создать словарь":
        dict_commands_state.create_dict = True
        bot.send_message(
            message.from_user.id,
            "Отлично! Вводите название словаря",
            reply_markup=ReplyKeyboardRemove()
        )
    elif message.text.lower() == "удалить словарь":
        dict_commands_state.del_dict = True
        text = [f"{dicts.pk} - {dicts.name}" for dicts in
                Dictionary.objects.filter(tg_user__tg_user_ID=message.from_user.id).all()]
        bot.send_message(message.from_user.id, "Вводите ID(число) словаря")
        time.sleep(2)
        bot.send_message(
            message.from_user.id,
            "\n".join(text)
        )
    else:
        dict_commands_state.reset_state()
        start_reset(message)


@bot.message_handler(func=lambda state: dict_commands_state.dict_title)
def dict_title(message: Message):
    dict_commands_state.reset_state()
    check_dict = Dictionary.objects.filter(name=message.text, tg_user__tg_user_ID=message.from_user.id).first()
    if not check_dict:
        bot.send_message(message.from_user.id, "Такого словаря у вас нет!")
        start_reset(message)
        return
    data = [data.word.word for data in check_dict.dictionary_words.all()]
    if not data:
        bot.send_message(message.from_user.id, "Словарь пуст!")
        start_reset(message)
        return
    bot.send_message(message.from_user.id, "\n".join(data))
    start_reset(message)


@bot.message_handler(func=lambda state: dict_commands_state.create_dict)
def create_dict(message: Message):
    dict_commands_state.reset_state()
    if Dictionary.objects.filter(name=message.text):
        bot.send_message(message.from_user.id, "Словарь с таким названием уже есть!")
        start_reset(message)
        return
    get_user = TelegramProfile.objects.filter(tg_user_ID=message.from_user.id).first()
    Dictionary.objects.create(name=message.text, tg_user=get_user)
    bot.send_message(message.from_user.id, "Словарь создан!")
    start_reset(message)


@bot.message_handler(func=lambda state: dict_commands_state.del_dict)
def delete_dict(message: Message):
    try:
        check_dict = Dictionary.objects.filter(pk=int(message.text)).first()
        if not check_dict:
            bot.send_message(message.from_user.id, "Словарь с таким ID не найден!")
            return
        check_dict.delete()
        bot.send_message(message.from_user.id, "Словарь успешно удалён!")
    except ValueError:
        bot.send_message(message.from_user.id, "Вы вводили не число!")
    finally:
        dict_commands_state.reset_state()
        start_reset(message)


@bot.message_handler(func=lambda state: add_word_state.get_dict)
def get_dict_to_add_word(message: Message):
    add_word_state.get_dict = None
    try:
        check_dict = Dictionary.objects.filter(
            tg_user__tg_user_ID=message.from_user.id,
            pk=int(message.text)
        ).first()
        if not check_dict:
            bot.send_message(message.from_user.id, "Словарь с таким ID не найден!")
            add_word_state.reset_state()
            add_word_state.reset_data()
            start_reset(message)
            return
        add_word_state.dict_id_data = check_dict
        add_word_state.get_word = True
        text = [f"{word.pk} - {word.word}" for word in
                WordsHistory.objects.filter(tg_user__tg_user_ID=message.from_user.id).all()]
        bot.send_message(message.from_user.id, "Отлично! Вводите ID(номер) слово")
        time.sleep(1)
        bot.send_message(message.from_user.id, "\n".join(text))
    except ValueError:
        bot.send_message(message.from_user.id, "Это не число!")
        add_word_state.reset_data()
        add_word_state.reset_state()
        start_reset(message)


@bot.message_handler(func=lambda state: add_word_state.get_word)
def add_word_to_dict(message: Message):
    add_word_state.get_word = None
    try:
        check_word = WordsHistory.objects.filter(
            tg_user__tg_user_ID=message.from_user.id,
            pk=int(message.text)
        ).first()
        if check_word:
            DictionaryWords.objects.create(dictionary=add_word_state.dict_id_data, word=check_word)
            bot.send_message(message.from_user.id, "Успешно добавил!")
        else:
            bot.send_message(message.from_user.id, "Слово с таким ID не найдено!")
    except ValueError:
        bot.send_message(message.from_user.id, "Это не число!")
    finally:
        add_word_state.reset_state()
        add_word_state.reset_data()
        start_reset(message)
