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

ALLOWED_SIZES = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
ALLOWED_TYPES = ['ZIP HOODIE', 'HOODIE', 'SWEATSHIRT', 'JACKET', 'SWEATER', 'ZIP 1/4', 'T-SHIRT', 'SALE']

router = Router()

class ProductState(StatesGroup):
    name = State()
    price = State()
    condition = State()
    size = State()
    photo = State()
    prod_type = State()


@router.callback_query(F.data == 'add_product')
async def start_fsm(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer('Введите название товара(exit - выйти)')
    await state.set_state(ProductState.name)


@router.message(ProductState.name)
async def product_name(message: Message, state: FSMContext):
    if message.text != 'exit':
        await state.update_data(name=message.text)
        await message.answer('Введите цену товара')
        await state.set_state(ProductState.price)
    else:
        state.clear()
        message.answer('Добавление товара прекращено')

@router.message(ProductState.price)
async def product_price(message: Message, state: FSMContext):
    if message.text != 'exit':
        if (message.text.isdigit()):
            await state.update_data(price=int(message.text))
            await message.answer('Введите состояние товара')
            await state.set_state(ProductState.condition)
        else:
            await message.answer('Введено не число')
    else:
        state.clear()
        message.answer('Добавление товара прекращено')

@router.message(ProductState.condition)
async def product_condition(message: Message, state: FSMContext):
    if message.text != 'exit':
        await state.update_data(condition=message.text)
        await message.answer('Введите размер товара')
        await state.set_state(ProductState.size)
    else:
        state.clear()
        message.answer('Добавление товара прекращено')

@router.message(ProductState.size)
async def product_size(message: Message, state: FSMContext):
    if message.text != 'exit':
        if message.text.upper() in ALLOWED_SIZES:
            await state.update_data(size=message.text.upper())
            await message.answer('Введите фото товара')
            await state.set_state(ProductState.photo)
        else:
            await message.answer('Непрвильный размер')
    else:
        state.clear()
        message.answer('Добавление товара прекращено')

@router.message(ProductState.photo)
async def photo(message: Message, state: FSMContext, bot: Bot):
    if message.text != 'exit':
        if message.photo:
            print(message.photo)
            file_name = f"{PHOTO_DIR}/{message.photo[-1].file_id}.jpg"
            await state.update_data(photo=f'{message.photo[-1].file_id}.jpg')
            await bot.download(message.photo[-1], destination=file_name)
            await message.answer(f"Теперь введите тип одежды \n Предложенные типы: {','.join(ALLOWED_TYPES)}")
            await state.set_state(ProductState.prod_type)
        else:
            await message.answer("Введено не фото")
    else:
        state.clear()
        message.answer('Добавление товара прекращено')


@router.message(ProductState.prod_type)
async def product_size(message: Message, state: FSMContext):
    if message.text != 'exit':
        if message.text.upper() in ALLOWED_TYPES:
            await state.update_data(prod_type=message.text.upper())
            data = await state.get_data()
            db.add_product(data['name'], data['price'], data['condition'], data['size'], data['photo'], data['prod_type'])
            await message.answer("Товар добавлен")
            await state.clear()
        else:
            await message.answer('Непрвильный размер')
    else:
        state.clear()
        message.answer('Добавление товара прекращено')