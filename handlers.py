from aiogram import F, Router
from aiogram.fsm.context import FSMContext #fsm нужен чтобы цправлять состояниями
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import keyboards


user = Router()

# @user.message()
# async def echo(message:Message):
#     await message.send_copy(chat_id=message.from_user.id) эхо


@user.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer("Добро пожаловать в BookWiseBot", reply_markup=keyboards.menu)

@user.message(F.text == 'Как это работает?')
async def cmd_help(message:Message):
    text = """
    📚 <b>Как работает BookWiseBot:</b>

    1. Ты присылаешь любую цитату из книги
    2. Бот отправляет её в нейросеть GigaChat
    3. GigaChat определяет:
    • Название книги
    • Автора
    • Смысл цитаты
    4. Бот показывает результат и предлагает:
    • Сохранить в избранное ❤️
    • Найти похожие книги 📖

    Просто отправь цитату и увидишь магию! ✨
        """
    await message.answer(text,parse_mode='HTML')