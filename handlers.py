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

@user.message(F.text == 'Избранное')
async def cmd_save(message: Message):
    await message.answer("Избарнное добавим попозже после БД")


@user.message(F.text)
async def cmd_text(message: Message):
    text = "ИИ чат сделает"
    await message.bot.send_chat_action(message.chat.id, action="typing")
    await message.answer(text, parse_mode='HTML')

@user.callback_query(F.data.startswith('zitata'))
async def zitatka(callback: CallbackQuery):
    zitata_keyboard = callback.data.split('_')[1]
    if zitata_keyboard == 'save':
        await callback.answer("❤️ Функция сохранения появится позже!", show_alert=False)
    elif zitata_keyboard == 'pohoji':
        await callback.answer("📚 Функция похожих книг в разработке!", show_alert=False)

    await callback.answer()
