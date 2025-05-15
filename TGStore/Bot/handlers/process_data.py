from aiogram import Router, F, Bot
from aiogram.types import Message, ContentType
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import FSInputFile
import json
import sys
import os

sys.path.insert(1, os.getcwd())

from Data.db import DataBase

BASE_DIR = os.path.abspath("Data")
PHOTO_DIR = os.path.join(os.path.abspath('Web_App'), 'static')
DB_DIR = os.path.join(BASE_DIR, 'store.db')
db = DataBase(DB_DIR)

from keyboards.delete_item_keyboard import get_delete_kb
router = Router()
ADMIN_CHAT = -1002350979236


@router.message(F.content_type == ContentType.WEB_APP_DATA)
async def parse_data(message: Message, bot: Bot):
    data = message.web_app_data.data
    procesed_data = json.loads( data )
    await message.answer('Менеджер с вами свяжется')
    print(procesed_data)
    media_group = MediaGroupBuilder()
    caption_text = ''
    for prod_id in procesed_data[-1]:
        prod_data = db.get_by_id(prod_id)
        caption_text += f'Название: {prod_data[1]} Цена: {prod_data[2]}  Состояние: {prod_data[3]} Размер: {prod_data[4]} \n'
    for i in range(len(procesed_data[-1])):
        prod_data = db.get_by_id(procesed_data[-1][i])
        if procesed_data[1] == "Самовывоз":
            if i == 0:
                media_group.add_photo(type="photo", caption=f"""Оплата: {procesed_data[0]} \n Способ доставки: {procesed_data[1]} \n Имя: {procesed_data[2]} \n Телефон: {procesed_data[3]} \n Телеграм: {procesed_data[4]}
                                        \n Bucket:\n{caption_text}""", media=FSInputFile(f'{PHOTO_DIR}/{prod_data[5]}'))
            else:
                media_group.add_photo(type="photo", media=FSInputFile(f'{PHOTO_DIR}/{prod_data[5]}'))
        else:
            if i == 0:
                media_group.add_photo(type="photo", caption=f"""Оплата: {procesed_data[0]} \n Способ доставки: {procesed_data[1]} \n Имя: {procesed_data[2]} \n Телефон: {procesed_data[3]} 
                                        \n Адрес: {procesed_data[4]} \n Комментарий: {procesed_data[5]} \n Телеграм: {procesed_data[6]}
                                        \n Bucket: \n {caption_text}""", media=FSInputFile(f'{PHOTO_DIR}/{prod_data[5]}'))
            else:
                media_group.add_photo(type="photo", media=FSInputFile(f'{PHOTO_DIR}/{prod_data[5]}'))
    await bot.send_media_group(ADMIN_CHAT, media=media_group.build())
    await bot.send_message(ADMIN_CHAT, 'Закрыть заказ', reply_markup=get_delete_kb('.'.join(procesed_data[-1])))