def extract_book_info_simple(text: str) -> dict:
    """
    Извлекает название книги и автора из ответа GigaChat.
    Простой способ без регулярных выражений.
    
    Args:
        text (str): Ответ от GigaChat
        
    Returns:
        dict: Словарь с ключами 'title' и 'author'
    """
    # Значения по умолчанию
    result = {
        'title': 'Не удалось определить',
        'author': 'Не удалось определить'
    }
    
    # Разбиваем текст на строки
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Ищем строку с названием книги
        if 'Название книги:' in line:
            # Берём всё после двоеточия
            title = line.split('Название книги:')[-1]
            # Убираем HTML-теги
            title = title.replace('<b>', '').replace('</b>', '').strip()
            result['title'] = title
        
        # Ищем строку с автором
        if 'Автор:' in line:
            # Берём всё после двоеточия
            author = line.split('Автор:')[-1]
            # Убираем HTML-теги
            author = author.replace('<b>', '').replace('</b>', '').strip()
            result['author'] = author
    
    return result


def extract_similar_books_simple(text: str) -> list:
    """
    Извлекает список похожих книг из ответа GigaChat.
    Простой способ без регулярных выражений.
    
    Args:
        text (str): Ответ от GigaChat со списком книг
    
    Returns:
        list: Список словарей с книгами
    """
    books = []
    
    # Разбиваем текст на строки
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Ищем строки, которые начинаются с маркера списка
        if line.startswith('•'):
            # Убираем маркер
            line = line.replace('•', '').strip()
            
            # Ищем тире
            if '—' in line:
                parts = line.split('—')
                if len(parts) == 2:
                    # Первая часть - название (с HTML-тегами)
                    title_part = parts[0].strip()
                    author_part = parts[1].strip()
                    
                    # Убираем HTML-теги из названия
                    title = title_part.replace('<b>', '').replace('</b>', '').strip()
                    
                    books.append({
                        'title': title,
                        'author': author_part
                    })
    
    return books
