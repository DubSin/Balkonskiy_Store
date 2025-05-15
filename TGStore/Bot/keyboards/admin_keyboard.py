from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Добавить новый товар", callback_data='add_product')
    kb.button(text="Удалить товар", callback_data='delete_product')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)