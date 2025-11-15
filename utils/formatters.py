"""
Форматирование отображения для приложения переназначения клавиш.
"""

from constants import SYMBOL_CATEGORIES, CURRENCIES


def format_key_display(key: str) -> str:
    """Форматирует клавишу для отображения."""
    if '+' in key:
        parts = key.split('+')
        return '+'.join(part.capitalize() for part in parts)
    elif key.startswith('f'):
        return key.upper()
    elif len(key) == 1:
        return key.upper()
    else:
        return key.capitalize()


def get_action_display(action: str) -> str:
    """Получить отображаемое название действия."""
    action_handlers = {
        'date_long': "Дата (длинная)",
        'date_short': "Дата (короткая)",
        'datetime': "Дата и время",
        'time': "Время"
    }

    if action in action_handlers:
        return action_handlers[action]
    elif action.startswith('currency:'):
        return _format_currency_display(action)
    elif action.startswith('symbol:'):
        return _format_symbol_display(action)
    elif action.startswith('"""') and action.endswith('"""'):
        return _format_multiline_display(action)
    elif action.startswith('"') and action.endswith('"'):
        return _format_text_display(action)
    else:
        return action


def _format_currency_display(action: str) -> str:
    """Форматирование отображения валюты."""
    currency = action.replace('currency:', '')
    currency_names = {
        'ruble': '₽ Рубль',
        'tenge': '₸ Тенге',
        'dram': '֏ Драм',
        'som': 'Soʻm Сумы'
    }
    return currency_names.get(currency.lower(), f'Валюта: {currency}')


def _format_symbol_display(action: str) -> str:
    """Форматирование отображения символа."""
    symbol_name = action.replace('symbol:', '')
    symbol_display = {
        'plus': '+ Плюс',
        'minus': '- Минус',
        'multiply': '* Умножить',
        'divide': '/ Разделить',
        'equals': '= Равно',
        'arrow_left': '← Стрелка влево',
        'arrow_right': '→ Стрелка вправо',
        'arrow_up': '↑ Стрелка вверх',
        'arrow_down': '↓ Стрелка вниз',
        'copyright': '© Копирайт',
        'registered': '® Зарегистрировано',
        'trademark': '™ Торговая марка',
        'degree': '° Градус',
        'euro': '€ Евро',
        'pound': '£ Фунт',
        'yen': '¥ Йена',
        'check': '✓ Галочка',
        'star': '★ Звезда',
        'heart': '♥ Сердце'
    }
    return symbol_display.get(symbol_name.lower(), f'Символ: {symbol_name}')


def _format_text_display(action: str) -> str:
    """Форматирование отображения текста."""
    text = action[1:-1]
    preview = text[:20] + "..." if len(text) > 20 else text
    return f'Текст: "{preview}"'


def _format_multiline_display(action: str) -> str:
    """Форматирование отображения многострочного текста."""
    text = action[3:-3]
    preview = text[:20] + "..." if len(text) > 20 else text
    return f'Многострочный: "{preview}"'