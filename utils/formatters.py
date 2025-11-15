"""
Форматирование данных для отображения.
"""
from typing import Dict, Any
from constants import CURRENCY_SYMBOLS, ASCII_SYMBOLS


class DisplayFormatter:
    """Класс для форматирования данных для отображения."""

    @staticmethod
    def format_key_display(key: str) -> str:
        """
        Форматирует клавишу для отображения.

        Args:
            key: Клавиша или комбинация

        Returns:
            Отформатированное отображение клавиши
        """
        if not key:
            return ""

        if '+' in key:
            parts = key.split('+')
            return '+'.join(p.capitalize() for p in parts)
        elif key.startswith('f'):
            return key.upper()
        elif len(key) == 1:
            return key.upper()
        else:
            return key.capitalize()

    @staticmethod
    def get_action_display(action: str) -> str:
        """
        Получает читаемое отображение действия.

        Args:
            action: Действие из конфигурации

        Returns:
            Человеко-читаемое описание действия
        """
        if not action:
            return "Неизвестное действие"

        action_handlers = {
            'date_long': lambda: "Дата (длинная)",
            'date_short': lambda: "Дата (короткая)",
            'datetime': lambda: "Дата и время",
            'time': lambda: "Время",
        }

        # Обработка специальных действий
        if action in action_handlers:
            return action_handlers[action]()

        # Обработка валют
        if action.startswith('currency:'):
            currency = action.replace('currency:', '')
            symbol = CURRENCY_SYMBOLS.get(currency.lower(), '')
            currency_names = {
                'ruble': 'Рубль', 'tenge': 'Тенге',
                'dram': 'Драм', 'som': 'Сумы'
            }
            name = currency_names.get(currency.lower(), currency)
            return f"{symbol} {name}" if symbol else name

        # Обработка символов
        if action.startswith('symbol:'):
            symbol_name = action.replace('symbol:', '')
            symbol = ASCII_SYMBOLS.get(symbol_name.lower(), '')
            symbol_display_names = {
                'plus': 'Плюс', 'minus': 'Минус', 'multiply': 'Умножить',
                'divide': 'Разделить', 'equals': 'Равно', 'arrow_left': 'Стрелка влево',
                'arrow_right': 'Стрелка вправо', 'arrow_up': 'Стрелка вверх',
                'arrow_down': 'Стрелка вниз', 'copyright': 'Копирайт',
                'registered': 'Зарегистрировано', 'trademark': 'Торговая марка',
                'degree': 'Градус', 'euro': 'Евро', 'pound': 'Фунт',
                'yen': 'Йена', 'check': 'Галочка', 'star': 'Звезда', 'heart': 'Сердце'
            }
            display_name = symbol_display_names.get(symbol_name.lower(), f'Символ: {symbol_name}')
            return f"{symbol} {display_name}" if symbol else display_name

        # Обработка многострочного текста
        if action.startswith('"""') and action.endswith('"""'):
            text = action[3:-3]
            preview = text[:20] + "..." if len(text) > 20 else text
            return f'Многострочный: "{preview}"'

        # Обработка обычного текста
        if action.startswith('"') and action.endswith('"'):
            text = action[1:-1]
            preview = text[:20] + "..." if len(text) > 20 else text
            return f'Текст: "{preview}"'

        # Комбинация клавиш
        return f"Клавиши: {action}"

    @staticmethod
    def format_profile_info(profile_name: str, mappings_count: int,
                            target_process: str, is_current: bool = False) -> str:
        """
        Форматирует информацию о профиле для отображения.

        Args:
            profile_name: Имя профиля
            mappings_count: Количество назначений
            target_process: Целевой процесс
            is_current: Является ли текущим

        Returns:
            Отформатированная строка информации о профиле
        """
        marker = "👉" if is_current else "  "
        return f"{marker} {profile_name} - {mappings_count} назначений, процесс: {target_process}"

    @staticmethod
    def format_process_status(process_name: str, target_process: str,
                              is_match: bool) -> str:
        """
        Форматирует статус процесса для отображения.

        Args:
            process_name: Имя активного процесса
            target_process: Целевой процесс
            is_match: Совпадает ли активный процесс с целевым

        Returns:
            Отформатированная строка статуса процесса
        """
        status_icon = "✅" if is_match else "❌"
        process_display = process_name or "Не определен"
        return f"{status_icon} {process_display}"