"""
Константы приложения переназначения клавиш.
"""

import os

# Пути и файлы
CONFIG_FILE = "key_config.json"
BACKUP_DIR = "backups"

# Значения по умолчанию
DEFAULT_TARGET_PROCESS = "browser.exe"
DEFAULT_PROFILE = "default"

# Интервалы проверок (секунды)
PROCESS_CHECK_INTERVAL = 0.1
PROCESS_MONITOR_INTERVAL = 0.2

# Проверка доступности Windows API
try:
    import win32gui
    import win32process
    import psutil
    WINDOWS_API_AVAILABLE = True
except ImportError:
    WINDOWS_API_AVAILABLE = False

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
            ('en_dash', '—', 'Короткое тире')
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

# Новые возможности
FEATURE_FLAGS = {
    'AUTO_START': True,
    'QUICK_PROFILES': True,
    'MACRO_RECORDING': True,
    'PROCESS_FILTERS': True,
    'BACKUP_MANAGEMENT': True
}

# Быстрые профили
QUICK_PROFILES = {
    'web_browser': {
        'name': 'Веб-браузер',
        'target_process': 'chrome.exe',
        'preset_mappings': {
            'ctrl+t': '"Новая вкладка"',
            'ctrl+w': '"Закрыть вкладку"',
            'ctrl+shift+t': '"Восстановить вкладку"',
            'f5': '"Обновить страницу"'
        }
    },
    'text_editor': {
        'name': 'Текстовый редактор',
        'target_process': 'notepad.exe',
        'preset_mappings': {
            'ctrl+s': '"Сохранить документ"',
            'ctrl+b': 'symbol:bullet',
            'f12': '"Вставка даты"'
        }
    },
    'code_editor': {
        'name': 'Редактор кода',
        'target_process': 'code.exe',
        'preset_mappings': {
            'ctrl+shift+`': '"Открыть терминал"',
            'f5': '"Запуск отладки"',
            'ctrl+shift+f': '"Поиск по проекту"'
        }
    }
}

# Макросы
DEFAULT_MACROS = {
    'email_signature': {
        'name': 'Подпись email',
        'text': 'С уважением,\n[Ваше Имя]\n[Ваша Должность]'
    },
    'current_datetime': {
        'name': 'Текущие дата и время',
        'action': 'datetime'
    },
    'separator': {
        'name': 'Разделитель',
        'text': '---'
    }
}

# Расширенные настройки
ADVANCED_SETTINGS = {
    'typing_delay': 0.01,
    'clipboard_timeout': 0.05,
    'process_check_frequency': 0.1,
    'max_backup_files': 10
}