import aiosqlite


DB_PATH = "bookwise.db"

# Инициализация базы данных
async def init_db():
    """Создает таблицу favorites, если её нет"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                quote TEXT NOT NULL,
                book_title TEXT NOT NULL,
                author TEXT NOT NULL
            )
        """)
        await db.commit()
    print("✅ База данных инициализирована (асинхронно)")

# Добавление в избранное
async def add_favorite(user_id: int, quote: str, book_title: str, author: str):
    """Добавляет цитату в избранное"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO favorites (user_id, quote, book_title, author) VALUES (?, ?, ?, ?)",
            (user_id, quote, book_title, author)
        )
        await db.commit()
        return cursor.lastrowid

# Получение всех избранных цитат пользователя
async def get_favorites(user_id: int):
    """Получает все избранные цитаты пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id, quote, book_title, author FROM favorites WHERE user_id = ? ORDER BY id DESC",
            (user_id,)
        )
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

#Удаление цитаты по ID
async def delete_favorite(user_id: int, quote_id: int):
    """Удаляет цитату из избранного"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM favorites WHERE id = ? AND user_id = ?",
            (quote_id, user_id)
        )
        await db.commit()
        return cursor.rowcount > 0
    
async def check_duplicate(user_id: int, quote: str, book_title: str, author: str):
    """Проверяет, есть ли уже такая цитата у пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id FROM favorites WHERE user_id = ? AND quote = ? AND book_title = ? AND author = ?",
            (user_id, quote, book_title, author)
        )
        existing = await cursor.fetchone()
        await cursor.close()
        return existing is not None  # True если уже есть