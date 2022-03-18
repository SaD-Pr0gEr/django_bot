from googletrans import Translator
from telebot.types import Message, ReplyKeyboardRemove

from main.bot.archive.keyboards_archive import language_keyboards
from main.bot.archive.states_archive import translate_commands_state
from main.bot.handlers.users.start import start_reset
from main.bot.loader import bot
from telegram.models import TelegramProfile
from translator.models import Languages, WordsHistory


@bot.message_handler(func=lambda state: translate_commands_state.from_language)
def from_language(message: Message):
    translate_commands_state.from_language = None
    check_language = Languages.objects.filter(language__iexact=message.text).first()
    if not check_language:
        bot.send_message(
            message.from_user.id,
            "Язык не найден!",
            reply_markup=ReplyKeyboardRemove()
        )
        translate_commands_state.reset_data()
        translate_commands_state.reset_state()
        start_reset(message)
        return
    translate_commands_state.from_language_data = check_language
    text = [
        "Отлично!",
        "На какой язык перевести?"
    ]
    bot.send_message(
        message.from_user.id,
        "\n".join(text),
        reply_markup=language_keyboards
    )
    translate_commands_state.to_language = True


@bot.message_handler(func=lambda state: translate_commands_state.to_language)
def to_language(message: Message):
    translate_commands_state.to_language = None
    check_language = Languages.objects.filter(language__iexact=message.text).first()
    if not check_language:
        bot.send_message(
            message.from_user.id,
            "Язык не найден!",
            ReplyKeyboardRemove()
        )
        translate_commands_state.reset_data()
        translate_commands_state.reset_state()
        start_reset(message)
        return
    translate_commands_state.to_language_data = check_language
    translate_commands_state.word_state = True
    text = [
        "Отлично!",
        "Вводите слово для перевода",
    ]
    bot.send_message(
        message.from_user.id,
        "\n".join(text),
        reply_markup=ReplyKeyboardRemove()
    )


@bot.message_handler(func=lambda state: translate_commands_state.word_state)
def word(message: Message):
    translate_commands_state.word_state = None
    translate_word = Translator().translate(
        message.text,
        dest=translate_commands_state.to_language_data.code_for_translator,
        src=translate_commands_state.from_language_data.code_for_translator
    )
    response = [
        "Перевод:",
        f"{translate_word.text}",
    ]
    bot.send_message(
        message.from_user.id,
        "\n".join(response),
    )
    get_user = TelegramProfile.objects.filter(tg_user_ID=message.from_user.id).first()
    text = [
        "Идеально!",
        "Перевод сохранён в историю...",
        "Также можете её увидеть с истории на нашем сайте"
    ]
    bot.send_message(message.from_user.id, "\n".join(text))
    WordsHistory.objects.create(
        word=message.text,
        value=translate_word.text,
        tg_user=get_user,
        language=translate_commands_state.from_language_data,
        to_language=translate_commands_state.to_language_data
    )
    translate_commands_state.reset_data()
    translate_commands_state.reset_state()
    start_reset(message)
