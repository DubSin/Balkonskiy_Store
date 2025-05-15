import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import to_web_app, admin, add_product, process_data, del_item_from_admin, del_item_from_group
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
TOKEN = os.getenv('TOKEN')

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_routers(to_web_app.router, admin.router, add_product.router, process_data.router, del_item_from_admin.router, del_item_from_group.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())