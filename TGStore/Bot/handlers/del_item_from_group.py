from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram import Bot
import sys
import os

sys.path.insert(1, os.getcwd())

from Data.db import DataBase

BASE_DIR = os.path.abspath("Data")
PHOTO_DIR = os.path.join(os.path.abspath('Web_App'), 'static')
DB_DIR = os.path.join(BASE_DIR, 'store.db')
db = DataBase(DB_DIR)

router = Router()


@router.callback_query(F.data.startswith('delete_product_ingroup/'))
async def start_fsm(callback_query: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback_query.id)
    products_id_list = [int(i) for i in callback_query.data.split('/')[1].split('.')]
    for product_id in products_id_list:
        product_data = db.get_by_id(product_id)
        if product_data:
            db.delete_product(product_data[1])
    await bot.edit_message_text(callback_query.message.chat.id, callback_query.message.message_id, text='Заказ закрыт', reply_markup=None)
