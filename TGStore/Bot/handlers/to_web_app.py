from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.web_app_keyboard import get_web_app_kb

router = Router()

@router.message(Command(commands='start'))
async def count_price(message: Message):
    await message.answer('Приветствуем в боте', reply_markup=get_web_app_kb())