from telebot.types import KeyboardButton


def conf_buttons(buttons_list: list):
    return [KeyboardButton(text=button) for button in buttons_list]
