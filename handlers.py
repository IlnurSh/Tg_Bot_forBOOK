from aiogram import F, Router
from aiogram.fsm.context import FSMContext #fsm нужен чтобы цправлять состояниями
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

user = Router()

@user.message()
async def echo(message:Message):
    await message.send_copy(chat_id=message.from_user.id)