from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Как это работает?')],
        [KeyboardButton(text='Избранное')]
    ],
    resize_keyboard=True#не широка клава
)