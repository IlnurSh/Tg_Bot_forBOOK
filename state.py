from aiogram.fsm.state import State, StatesGroup

class BookData(StatesGroup):
    title = State()   # название книги
    author = State()  # автор
    quote = State()   # цитата

class FavoritesData(StatesGroup):
    action = State() #какое либо действие по типу удалить изменить показать
    book_id = State() #id книги в избранном
