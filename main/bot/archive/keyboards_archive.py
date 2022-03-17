from main.bot.buttons.start_commands import start_menu_buttons
from main.bot.keybhoards.default.configure import ConfigureKeyboards
from translator.models import Languages

start_keyboards = ConfigureKeyboards(start_menu_buttons(["Словарь", "Переводчик"]), resize=True)
language_keyboards = ConfigureKeyboards(start_menu_buttons(
    [data.language for data in Languages.objects.all()]),
    resize=True
)
