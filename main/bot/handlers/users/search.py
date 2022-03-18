import time

from telebot.types import Message, ReplyKeyboardRemove

from main.bot.archive.states_archive import search_commands_state
from main.bot.handlers.users.start import start_reset
from main.bot.loader import bot
from translator.models import WordsHistory


@bot.message_handler(func=lambda state: search_commands_state.search_type)
def search(message: Message):
    search_commands_state.search_type = None
    if message.text.lower() == "по первой букве":
        search_commands_state.by_first = True
    elif message.text.lower() == "по совпадению букв":
        search_commands_state.icontains = True
    elif message.text.lower() == "строго по словам":
        search_commands_state.iexact = True
    else:
        search_commands_state.reset_state()
        start_reset(message)
    bot.send_message(
        message.from_user.id,
        "Круто! Вводите букву(или слово)",
        reply_markup=ReplyKeyboardRemove()
    )


@bot.message_handler(func=lambda state: search_commands_state.by_first)
def by_first(message: Message):
    search_commands_state.reset_state()
    if len(message.text.split()) > 1 or len(message.text) > 1:
        bot.send_message(message.from_user.id, "Ору... вам говорили вводить 1 букву 🌚")
        time.sleep(1)
        start_reset(message)
        return
    text = [words.word for words in WordsHistory.objects.filter(
        word__startswith=message.text,
        tg_user__tg_user_ID=message.from_user.id
    ).all()]
    if text:
        bot.send_message(message.from_user.id, "Результат:")
        bot.send_message(message.from_user.id, "\n".join(text))
    else:
        bot.send_message(message.from_user.id, f"Слова начинающие с {message.text} не найдены!")
    start_reset(message)


@bot.message_handler(func=lambda state: search_commands_state.icontains)
def icontains(message: Message):
    search_commands_state.reset_state()
    text = [word.word for word in WordsHistory.objects.filter(
        word__icontains=message.text,
        tg_user__tg_user_ID=message.from_user.id
    ).all()]
    if text:
        bot.send_message(message.from_user.id, "Результат:")
        bot.send_message(message.from_user.id, "\n".join(text))
    else:
        bot.send_message(message.from_user.id, f"Слова с буквой {message.text} не найдены!")
    start_reset(message)


@bot.message_handler(func=lambda state: search_commands_state.iexact)
def iexact(message: Message):
    search_commands_state.reset_state()
    text = [word.word for word in WordsHistory.objects.filter(
        word__iexact=message.text,
        tg_user__tg_user_ID=message.from_user.id
    ).all()]
    if text:
        bot.send_message(message.from_user.id, "Результат:")
        bot.send_message(message.from_user.id, "\n".join(text))
    else:
        bot.send_message(message.from_user.id, f"Слова с буквой {message.text} не найдены!")
    start_reset(message)
