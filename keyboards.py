from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton,InlineKeyboardMarkup

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Как это работает?')],
        [KeyboardButton(text='Избранное')]
    ],
    resize_keyboard=True#не широка клава
)

zizata = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='❤️ Добавить в избранное', callback_data='zitata_save')],
        [InlineKeyboardButton(text='📚 3 похожие книги', callback_data='zitata_pohoji')]
    ]
)