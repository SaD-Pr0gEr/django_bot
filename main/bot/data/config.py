import os

from dotenv import load_dotenv
from telebot import TeleBot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = os.getenv("ADMIN_IDS")


def create_bot(bot_token: str) -> TeleBot:
    create = TeleBot(token=bot_token)
    return create
