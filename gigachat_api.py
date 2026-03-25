import os
import aiohttp
import asyncio
import uuid
import base64
import ssl
from dotenv import load_dotenv


# Загружаем переменные окружения
load_dotenv()

# 👇 ОТЛАДКА ПЕРЕМЕННЫХ
print(f"🔍 CLIENT_ID: {os.getenv('GIGACHAT_CLIENT_ID')}")
print(f"🔍 CLIENT_SECRET: {os.getenv('GIGACHAT_SECRET')[:10] if os.getenv('GIGACHAT_SECRET') else 'None'}...")

CLIENT_ID = os.getenv('GIGACHAT_CLIENT_ID')
CLIENT_SECRET = os.getenv('GIGACHAT_SECRET')

# URL и настройки
AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
CHAT_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
MODEL_NAME = "GigaChat-2-Max"

# Настройки SSL
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Создаём Basic Auth строку
auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
GIGACHAT_AUTH = base64.b64encode(auth_string.encode()).decode()


async def get_access_token() -> str:
    headers = {
        'Authorization': f'Basic {GIGACHAT_AUTH}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4())
    }
    
    data = {'scope': 'GIGACHAT_API_PERS'}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(AUTH_URL, headers=headers, data=data, ssl=ssl_context) as response:
            if response.status != 200:
                raise Exception(f"Ошибка авторизации: {response.status}")
            
            result = await response.json()
            return result['access_token']


async def get_book_info(quote: str) -> str:
    try:
        print(f"🔍 get_book_info вызвана для: {quote[:50]}...")  # 👈 ОТЛАДКА
        
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
            "max_tokens": 400
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(CHAT_URL, headers=headers, json=data, ssl=ssl_context) as response:
                if response.status != 200:
                    print(f"❌ Ошибка API: {response.status}")  # 👈 ОТЛАДКА
                    return f"❌ Ошибка API: {response.status}"
                
                result = await response.json()
                print(f"✅ Ответ получен, длина: {len(result['choices'][0]['message']['content'])}")  # 👈 ОТЛАДКА
                return result['choices'][0]['message']['content']
    
    except Exception as e:
        print(f"❌ ОШИБКА В get_book_info: {e}")  # 👈 ОТЛАДКА
        return "❌ Не удалось определить книгу"


async def get_similar_books(book_title: str, author: str) -> str:
    try:
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
            "max_tokens": 400
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(CHAT_URL, headers=headers, json=data, ssl=ssl_context) as response:
                if response.status != 200:
                    return f"❌ Ошибка API: {response.status}"
                
                result = await response.json()
                return result['choices'][0]['message']['content']
    
    except Exception as e:
        print(f"❌ ОШИБКА В get_similar_books: {e}")  # 👈 ОТЛАДКА
        return "❌ Не удалось найти похожие книги"
