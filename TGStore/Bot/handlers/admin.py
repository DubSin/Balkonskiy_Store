from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.admin_keyboard import get_admin_kb

router = Router()

from dotenv import load_dotenv, find_dotenv
import json
import os

load_dotenv(find_dotenv())
ADMIN_LIST = [int(i) for i in json.loads(os.getenv('ADMIN_LIST'))]

@router.message(Command(commands='admin'))
async def count_price(message: Message):
    if message.from_user.id in ADMIN_LIST:
        await message.reply('Админская панель', reply_markup=get_admin_kb())