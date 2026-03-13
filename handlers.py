from aiogram import F, Router
from aiogram.fsm.context import FSMContext #fsm нужен чтобы цправлять состояниями
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup

from gigachat_api import get_book_info, get_similar_books
import keyboards
from parsers import extract_book_info_simple
import database as db


class AddQuote(StatesGroup):
    waiting_for_quote = State()      # ждем текст цитаты
    waiting_for_book = State()       # ждем название книги
    waiting_for_author = State()     # ждем автора

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
    user_id = message.from_user.id
    favorites = await db.get_favorites(user_id)

    if not favorites:
        await message.answer("У вас нет избранных цитат пшл вн")
        return

    text = "твои избраные цитаты\n\n"
    for fav in favorites:
        id1 = fav[0]
        quote1 = fav[1]
        bookTitle1 = fav[2]
        author1 = fav[3]

        text += f"Id: {id1}\n"
        text += f"Цитата: {quote1}\n"
        text += f"Book: {bookTitle1}\n"
        text += f"Author: {author1}\n"
        text += f"----------------\n"

    await message.answer(text)

@user.message(F.text)
async def cmd_text(message: Message, state: FSMContext):
    await message.bot.send_chat_action(message.chat.id, action="typing")
    processing = await message.answer("🔍 Ищу информацию о книге...")
    try:
        result = await get_book_info(message.text)#ищет у ии ответ по промту 
        book_info = extract_book_info_simple(result) #вытаскивает название и автора
        
        await state.update_data( #сохраняет назване и автора
            quote=message.text,
            title=book_info['title'],
            author=book_info['author']
        )

        await processing.delete()
        await message.answer(result, parse_mode="HTML", reply_markup=keyboards.zizata)
    except Exception as e:
        await processing.delete()
        await message.answer(f"❌ Произошла ошибка")



@user.callback_query(F.data.startswith('zitata'))
async def zitatka(callback: CallbackQuery, state: FSMContext):
    zitata_keyboard = callback.data.split('_')[1]

    if zitata_keyboard == 'save':
        data = await state.get_data()
        
        if not data:
            return await callback.message.edit_text("❌ Ошибка: данные не найдены")
    
        # Проверка на дубликат
        is_duplicate = await db.check_duplicate(
            user_id=callback.from_user.id,
            quote=data['quote'],
            book_title=data['title'],
            author=data['author']
        )
        
        if is_duplicate:
            await callback.message.answer("⚠️ Эта цитата уже есть в избранном!")
            await callback.answer()
            return
        
        await db.add_favorite(
            user_id=callback.from_user.id,
            quote=data['quote'], 
            book_title=data['title'],
            author=data['author']
        )

    elif zitata_keyboard == 'pohoji':
        data = await state.get_data()
        title = data.get('title')
        author = data.get('author')
        
        if not title or title == 'Не удалось определить':
            await callback.answer("❌ Цитату не удалось определить, напиши ее заново!", show_alert=False)
            return
        
        await callback.answer("🔍 Ищу похожие книги...")
        
        processing = await callback.message.answer("🔍 Ищу похожие книги...")
        
        try:
            result = await get_similar_books(title, author)
            await processing.delete()
            await callback.message.answer(result, parse_mode="HTML")
        except Exception as e:
            await processing.delete()
            await callback.message.answer("❌ Ошибка")
