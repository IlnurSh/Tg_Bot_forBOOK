import sqlite3
import aiosqlite

DB_PATH = "bookwise.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # Таблица для избранных цитат
        await db.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                quote TEXT NOT NULL,
                book_title TEXT NOT NULL,
                author TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.commit()
    print("✅ База данных инициализирована")


# ---------- РАБОТА С ИЗБРАННЫМ ----------
async def add_favorite(user_id: int, quote: str, book_title: str, author: str) -> bool:
    """
    Добавляет цитату в избранное пользователя.
    Возвращает True при успехе, False при ошибке.
    """
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO favorites (user_id, quote, book_title, author) VALUES (?, ?, ?, ?)",
                (user_id, quote, book_title, author)
            )
            await db.commit()
            return True
    except Exception as e:
        print(f"❌ Ошибка при добавлении в избранное: {e}")
        return False


async def get_favorites(user_id: int) -> list:
    """
    Возвращает список избранных цитат пользователя.
    Каждый элемент: (id, quote, book_title, author, created_at)
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id, quote, book_title, author, created_at FROM favorites WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        rows = await cursor.fetchall()
        return rows


async def delete_favorite(favorite_id: int, user_id: int) -> bool:
    """
    Удаляет цитату из избранного по её ID.
    Проверяем user_id для безопасности (чтобы чужое не удалил).
    """
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "DELETE FROM favorites WHERE id = ? AND user_id = ?",
                (favorite_id, user_id)
            )
            await db.commit()
            return True
    except Exception as e:
        print(f"❌ Ошибка при удалении: {e}")
        return False


async def is_favorite_exists(user_id: int, quote: str) -> bool:
    """
    Проверяет, есть ли уже такая цитата в избранном у пользователя.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id FROM favorites WHERE user_id = ? AND quote = ?",
            (user_id, quote)
        )
        result = await cursor.fetchone()
        return result is not None


# ---------- ФОРМАТИРОВАНИЕ ДЛЯ ВЫВОДА ----------
def format_favorites(favorites: list) -> str:
    """
    Форматирует список избранного для красивого вывода.
    """
    if not favorites:
        return "❤️ У вас пока нет сохранённых цитат"
    
    text = "❤️ <b>Ваше избранное:</b>\n\n"
    for i, fav in enumerate(favorites, 1):
        fav_id, quote, title, author, date = fav
        text += f"{i}. <b>{title}</b> — {author}\n"
        text += f"   <i>\"{quote[:100]}{'...' if len(quote) > 100 else ''}\"</i>\n"
        text += f"   📅 {date[:10]}\n\n"
    
    return text