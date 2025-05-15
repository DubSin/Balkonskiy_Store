from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import WebAppInfo

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
FLASK_URL = os.getenv('FLASK_URL')

def get_web_app_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Открыть приложение', web_app=WebAppInfo(url=FLASK_URL))
    kb.button(text="Связаться с менеджером", url='https://t.me/Vakunan')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)