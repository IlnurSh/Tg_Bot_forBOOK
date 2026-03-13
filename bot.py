import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import user
import database as db

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(user)

async def main():

    await db.init_db()

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")