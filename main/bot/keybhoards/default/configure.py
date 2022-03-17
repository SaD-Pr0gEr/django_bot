from telebot.types import ReplyKeyboardMarkup


class ConfigureKeyboards(ReplyKeyboardMarkup):
    
    def __init__(self, buttons_list: list, resize: bool):
        super(ConfigureKeyboards, self).__init__(resize_keyboard=resize)
        self.__add_buttons(buttons_list)

    def __add_buttons(self, buttons_list: list):
        self.add(*buttons_list)
