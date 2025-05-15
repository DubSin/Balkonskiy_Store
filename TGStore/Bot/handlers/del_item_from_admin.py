from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
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

class DeleteState(StatesGroup):
    name = State()


@router.callback_query(F.data == 'delete_product')
async def start_fsm(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer('Введите название товара(exit - выйти)')
    await state.set_state(DeleteState.name)


@router.message(DeleteState.name)
async def product_name(message: Message, state: FSMContext):
    if message.text != 'exit':
        await state.update_data(name=message.text)
        data = await state.get_data()
        if (db.product_exist_by_name(data['name'])):
            db.delete_product(data['name'])
            await message.answer('Товар удален')
            await state.clear()
        else:
            await message.answer('Товар не найден \n Введите другое название товара')
    else:
        state.clear()
        message.answer('Добавление товара прекращено')