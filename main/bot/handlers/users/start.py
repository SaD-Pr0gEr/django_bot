from telebot.types import Message, ReplyKeyboardRemove

from main.bot.archive.keyboards_archive import start_keyboards, language_keyboards
from main.bot.archive.states_archive import start_commands_state, translate_commands_state
from main.bot.loader import bot
from translator.models import Languages


@bot.message_handler(['start'])
def start(message: Message):
    text = [
        "Привет! Я бот переводчик...",
        "Выбери опцию",
    ]
    start_commands_state.category = True
    bot.send_message(
        message.from_user.id,
        "\n".join(text),
        reply_markup=start_keyboards
    )


@bot.message_handler(func=lambda state: start_commands_state.category)
def translate(message: Message):
    start_commands_state.category = None
    if message.text.lower() == "переводчик":
        text = [
            "Круто!",
            "C какого языка перевести?"
        ]
        translate_commands_state.from_language = True
        markup = language_keyboards
    else:
        text = [
            "Функция пока в разработке...",
        ]
        markup = ReplyKeyboardRemove()
    bot.send_message(
        message.from_user.id,
        "\n".join(text),
        reply_markup=markup
    )


@bot.message_handler(func=lambda state: translate_commands_state.from_language)
def from_language(message: Message):
    translate_commands_state.from_language = None
    if not Languages.objects.filter(language__iexact=message.text):
        bot.send_message(
            message.from_user.id,
            "Язык не найден!",
            reply_markup=ReplyKeyboardRemove()
        )
        translate_commands_state.reset_data()
        return
    translate_commands_state.from_language_data = message.text
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
    if not Languages.objects.filter(language__iexact=message.text):
        bot.send_message(
            message.from_user.id,
            "Язык не найден!",
            reply_markup=ReplyKeyboardRemove()
        )
        translate_commands_state.reset_data()
        return
    translate_commands_state.to_language_data = message.text
    translate_commands_state.word = True
    text = [
        "Отлично!",
        "Вводите слово для перевода",
    ]
    bot.send_message(
        message.from_user.id,
        "\n".join(text),
        reply_markup=ReplyKeyboardRemove()
    )


@bot.message_handler(func=lambda state: translate_commands_state.word)
def word(message: Message):
    translate_commands_state.word = None
    text = [
        "Отлично!",
        "Вы дошли до конца!",
        "Ваши ответы",
        f"{translate_commands_state.from_language_data} - {translate_commands_state.to_language_data} - {message.text}",
    ]
    translate_commands_state.reset_data()
    bot.send_message(
        message.from_user.id,
        "\n".join(text),
        reply_markup=ReplyKeyboardRemove()
    )
