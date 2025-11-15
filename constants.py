"""
Константы и настройки приложения.
"""

# Константы путей
CONFIG_FILE = "key_config.json"
BACKUP_DIR = "backups"
DEFAULT_TARGET_PROCESS = "browser.exe"
DEFAULT_PROFILE = "default"

# Windows API для определения активного окна
try:
    import win32gui
    import win32process
    import psutil

    WINDOWS_API_AVAILABLE = True
except ImportError:
    WINDOWS_API_AVAILABLE = False

# Настройки производительности
PROCESS_CHECK_INTERVAL = 0.1  # секунды
PROCESS_MONITOR_INTERVAL = 0.2  # секунды

# Поддерживаемые специальные клавиши
SPECIAL_KEYS = [
    'space', 'enter', 'tab', 'backspace', 'delete', 'esc', 'escape',
    'up', 'down', 'left', 'right', 'home', 'end', 'page up', 'page down',
    'insert', 'print screen', 'scroll lock', 'pause', 'caps lock',
    'num lock', 'num 0', 'num 1', 'num 2', 'num 3', 'num 4', 'num 5',
    'num 6', 'num 7', 'num 8', 'num 9', 'num +', 'num -', 'num *', 'num /', 'num enter',
    'shift', 'ctrl', 'alt', 'win', 'menu'
]

# Модификаторы клавиш
KEY_MODIFIERS = ['ctrl', 'alt', 'shift', 'win']

# Категории символов
SYMBOL_CATEGORIES = {
    '1': {
        'name': 'Математические',
        'description': '(+, -, *, /, =, ≠, ≤, ≥, ≈, ±, ∞, π, ∑, ∫)',
        'symbols': [
            ('plus', '+', 'Плюс'),
            ('minus', '-', 'Минус'),
            ('multiply', '*', 'Умножить'),
            ('divide', '/', 'Разделить'),
            ('equals', '=', 'Равно'),
            ('not_equal', '≠', 'Не равно'),
            ('less_equal', '≤', 'Меньше или равно'),
            ('greater_equal', '≥', 'Больше или равно'),
            ('approx', '≈', 'Приблизительно'),
            ('plus_minus', '±', 'Плюс-минус'),
            ('infinity', '∞', 'Бесконечность'),
            ('pi', 'π', 'Пи'),
            ('sum', '∑', 'Сумма'),
            ('integral', '∫', 'Интеграл')
        ]
    },
    '2': {
        'name': 'Стрелки',
        'description': '(←, →, ↑, ↓, ↔, «, »)',
        'symbols': [
            ('arrow_left', '←', 'Влево'),
            ('arrow_right', '→', 'Вправо'),
            ('arrow_up', '↑', 'Вверх'),
            ('arrow_down', '↓', 'Вниз'),
            ('arrow_both', '↔', 'В обе стороны'),
            ('arrow_double_left', '«', 'Двойная влево'),
            ('arrow_double_right', '»', 'Двойная вправо')
        ]
    },
    '3': {
        'name': 'Специальные',
        'description': '(©, ®, ™, °, §, ¶, •, ·, …, —, –)',
        'symbols': [
            ('copyright', '©', 'Копирайт'),
            ('registered', '®', 'Зарегистрировано'),
            ('trademark', '™', 'Торговая марка'),
            ('degree', '°', 'Градус'),
            ('section', '§', 'Секция'),
            ('paragraph', '¶', 'Параграф'),
            ('bullet', '•', 'Маркер'),
            ('middle_dot', '·', 'Средняя точка'),
            ('ellipsis', '…', 'Многоточие'),
            ('em_dash', '—', 'Длинное тире'),
            ('en_dash', '–', 'Короткое тире')
        ]
    },
    '4': {
        'name': 'Кавычки',
        'description': '(", ", \', \')',
        'symbols': [
            ('quote_left', '"', 'Левая двойная'),
            ('quote_right', '"', 'Правая двойная'),
            ('quote_single_left', "'", 'Левая одинарная'),
            ('quote_single_right', "'", 'Правая одинарная')
        ]
    },
    '5': {
        'name': 'Валюты',
        'description': '(€, £, ¥, ¢)',
        'symbols': [
            ('euro', '€', 'Евро'),
            ('pound', '£', 'Фунт'),
            ('yen', '¥', 'Йена'),
            ('cent', '¢', 'Цент')
        ]
    },
    '6': {
        'name': 'Другие',
        'description': '(✓, ✗, ★, ♥, ♦, ♣, ♠)',
        'symbols': [
            ('check', '✓', 'Галочка'),
            ('cross', '✗', 'Крестик'),
            ('star', '★', 'Звезда'),
            ('heart', '♥', 'Сердце'),
            ('diamond', '♦', 'Бриллиант'),
            ('club', '♣', 'Трефы'),
            ('spade', '♠', 'Пики')
        ]
    }
}

# Валюты
CURRENCIES = [
    ('ruble', '₽', 'Рубль'),
    ('tenge', '₸', 'Тенге'),
    ('dram', '֏', 'Драм'),
    ('som', 'Soʻm', 'Сумы')
]

# ASCII символы
ASCII_SYMBOLS = {
    # Математические
    'plus': '+', 'minus': '-', 'multiply': '*', 'divide': '/',
    'equals': '=', 'not_equal': '≠', 'less_equal': '≤', 'greater_equal': '≥',
    'approx': '≈', 'plus_minus': '±', 'infinity': '∞', 'pi': 'π',
    'sum': '∑', 'integral': '∫',
    # Стрелки
    'arrow_left': '←', 'arrow_right': '→', 'arrow_up': '↑', 'arrow_down': '↓',
    'arrow_both': '↔', 'arrow_double_left': '«', 'arrow_double_right': '»',
    # Специальные
    'copyright': '©', 'registered': '®', 'trademark': '™', 'degree': '°',
    'section': '§', 'paragraph': '¶', 'bullet': '•', 'middle_dot': '·',
    'ellipsis': '…', 'em_dash': '—', 'en_dash': '–',
    # Кавычки
    'quote_left': '"', 'quote_right': '"',
    'quote_single_left': "'", 'quote_single_right': "'",
    # Другие
    'euro': '€', 'pound': '£', 'yen': '¥', 'cent': '¢',
    'check': '✓', 'cross': '✗', 'star': '★', 'heart': '♥',
    'diamond': '♦', 'club': '♣', 'spade': '♠'
}

# Символы валют
CURRENCY_SYMBOLS = {
    'ruble': '₽', 'tenge': '₸', 'dram': '֏', 'Soʻm': 'Сумы'
}

# Названия месяцев для форматирования даты
MONTHS = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}