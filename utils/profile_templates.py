"""
Шаблоны быстрых профилей для приложения переназначения клавиш.
"""

from typing import Dict, Any

# Расширенные шаблоны быстрых профилей
QUICK_PROFILE_TEMPLATES = {
    'web_browser': {
        'name': 'Веб-браузер',
        'description': 'Профиль для работы в браузере',
        'target_process': 'chrome.exe',
        'preset_mappings': {
            'ctrl+t': '"Новая вкладка"',
            'ctrl+w': '"Закрыть вкладку"',
            'ctrl+shift+t': '"Восстановить вкладку"',
            'ctrl+r': '"Обновить страницу"',
            'f5': '"Обновить страницу"',
            'ctrl+l': '"Выделить адресную строку"',
            'ctrl+d': '"Добавить в закладки"',
            'ctrl+h': '"История"'
        }
    },
    'text_editor': {
        'name': 'Текстовый редактор',
        'description': 'Профиль для работы с текстом',
        'target_process': 'notepad.exe',
        'preset_mappings': {
            'ctrl+s': '"Сохранить документ"',
            'ctrl+b': 'symbol:bullet',
            'f12': 'date_short',
            'ctrl+shift+d': 'datetime',
            'ctrl+shift+t': 'time'
        }
    },
    'code_editor': {
        'name': 'Редактор кода',
        'description': 'Профиль для программирования',
        'target_process': 'code.exe',
        'preset_mappings': {
            'ctrl+shift+`': '"Открыть терминал"',
            'f5': '"Запуск отладки"',
            'ctrl+shift+f': '"Поиск по проекту"',
            'ctrl+shift+p': '"Палитра команд"',
            'ctrl+k': 'symbol:copyright',
            'ctrl+shift+c': 'symbol:copyright'
        }
    },
    'office_suite': {
        'name': 'Офисные приложения',
        'description': 'Профиль для работы с документами',
        'target_process': 'winword.exe',
        'preset_mappings': {
            'ctrl+s': '"Сохранить документ"',
            'ctrl+p': '"Печать"',
            'f12': '"Сохранить как..."',
            'ctrl+shift+d': 'datetime',
            'ctrl+shift+t': 'time'
        }
    },
    'graphics_design': {
        'name': 'Графический дизайн',
        'description': 'Профиль для работы с графикой',
        'target_process': 'photoshop.exe',
        'preset_mappings': {
            'ctrl+s': '"Сохранить проект"',
            'ctrl+shift+s': '"Сохранить как..."',
            'f12': '"Экспортировать"',
            'ctrl+shift+c': 'symbol:copyright',
            'ctrl+shift+r': 'symbol:registered'
        }
    },
    'file_manager': {
        'name': 'Файловый менеджер',
        'description': 'Профиль для работы с файлами',
        'target_process': 'explorer.exe',
        'preset_mappings': {
            'f2': '"Переименовать"',
            'f5': '"Обновить"',
            'ctrl+n': '"Новая папка"',
            'ctrl+shift+n': '"Новый документ"'
        }
    }
}

def get_quick_profile_template(profile_id: str) -> Dict[str, Any]:
    """Возвращает шаблон быстрого профиля по ID."""
    return QUICK_PROFILE_TEMPLATES.get(profile_id, {})

def list_quick_profile_templates() -> list:
    """Возвращает список доступных шаблонов."""
    templates = []
    for template_id, template in QUICK_PROFILE_TEMPLATES.items():
        templates.append({
            'id': template_id,
            'name': template['name'],
            'description': template['description'],
            'target_process': template['target_process'],
            'mappings_count': len(template['preset_mappings'])
        })
    return templates