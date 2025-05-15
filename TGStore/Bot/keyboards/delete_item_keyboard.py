from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_delete_kb(item) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"Удалить Заказ", callback_data=f'delete_product_ingroup/{item}')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)