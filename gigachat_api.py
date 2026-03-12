import os
import aiohttp
import asyncio
import uuid
from dotenv import load_dotenv
import ssl
import certifi

# Загружаем переменные окружения
load_dotenv()
GIGACHAT_AUTH = os.getenv('GIGACHAT_AUTH_DATA')

# Настройки SSL для безопасного соединения
ssl_context = ssl.create_default_context(cafile=certifi.where())

AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
CHAT_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
MODEL_NAME = "GigaChat-2-Max"


async def get_access_token() -> str:
    """
    Получает токен доступа к GigaChat.
    Токен действует 30 минут.
    """
    headers = {
        'Authorization': f'Basic {GIGACHAT_AUTH}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4())  # Уникальный ID запроса
    }
    
    data = {'scope': 'GIGACHAT_API_PERS'}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(AUTH_URL, headers=headers, data=data, ssl=ssl_context) as response:
            if response.status != 200:
                raise Exception(f"Ошибка авторизации: {response.status}")
            
            result = await response.json()
            return result['access_token']


async def get_book_info(quote: str) -> str:
    """
    Определяет книгу по цитате.
        quote (str): Цитата из книги
        str: Информация о книге (название, автор, смысл)
    """
    try:
        # Получаем токен
        access_token = await get_access_token()
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        prompt = f"""
        Определи книгу по цитате: "{quote}"
        
        Ответь строго в следующем формате. Используй HTML-теги для форматирования:
        
        📖 <b>Название книги:</b> [только название книги]
        ✍️ <b>Автор:</b> [только имя автора]
        
        💭 <b>Смысл цитаты:</b>
        [2-3 предложения о том, что означает эта цитата в контексте книги]
        
        ВАЖНО: Не пиши ничего про похожие книги! Только то, что указано выше.
        """
        
        data = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5,
            "max_tokens": 600
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(CHAT_URL, headers=headers, json=data, ssl=ssl_context) as response:
                if response.status != 200:
                    error_text = await response.text()
                    return f"❌ Ошибка API: {response.status}"
                
                result = await response.json()
                return result['choices'][0]['message']['content']
    
    except Exception as e:
        return f"❌ Не удалось определить книгу: {str(e)}"


async def get_similar_books(book_title: str, author: str) -> str:
    """
    Находит похожие книги.
        book_title (str): Название исходной книги
        author (str): Автор исходной книги
        str: Список похожих книг с объяснениями
    """
    try:
        # Получаем токен
        access_token = await get_access_token()
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        prompt = f"""
        Найди 3 книги, похожие на "{book_title}" автора {author}.
        
        Ответь строго в следующем формате. Используй HTML-теги для форматирования:
        
        📚 <b>Похожие книги на "{book_title}":</b>
        
        • <b>[Название книги 1]</b> — [Автор]
          <i>Почему похожа:</i> [краткое объяснение]
        
        • <b>[Название книги 2]</b> — [Автор]
          <i>Почему похожа:</i> [краткое объяснение]
        
        • <b>[Название книги 3]</b> — [Автор]
          <i>Почему похожа:</i> [краткое объяснение]
        
        ВАЖНО: Книги должны быть реальными, известными произведениями.
        """
        
        data = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 600
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(CHAT_URL, headers=headers, json=data, ssl=ssl_context) as response:
                if response.status != 200:
                    error_text = await response.text()
                    return f"❌ Ошибка API: {response.status}"
                
                result = await response.json()
                return result['choices'][0]['message']['content']
    
    except Exception as e:
        return f"❌ Не удалось найти похожие книги: {str(e)}"
