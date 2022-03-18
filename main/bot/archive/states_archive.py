from main.bot.fsm.add_word_dict import AddWordDict
from main.bot.fsm.dicts_fsm import DictsState
from main.bot.fsm.search import SearchKeyboard
from main.bot.fsm.start_menu import FirstMenuState
from main.bot.fsm.translator_category import TranslateCategoryState

start_commands_state = FirstMenuState()
translate_commands_state = TranslateCategoryState()
dict_commands_state = DictsState()
search_commands_state = SearchKeyboard()
add_word_state = AddWordDict()
