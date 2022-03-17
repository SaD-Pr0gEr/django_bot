from telebot.types import KeyboardButton


def start_menu_buttons(buttons_list: list):
    return [KeyboardButton(text=button) for button in buttons_list]
