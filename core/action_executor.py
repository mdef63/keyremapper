"""
Исполнитель действий для приложения переназначения клавиш.
"""

import time
from datetime import datetime

try:
    import pyperclip
    import keyboard
except ImportError:
    pass  # Обработка ошибок будет в main


class ActionExecutor:
    """Выполнение различных типов действий."""

    def __init__(self):
        self._date_formats = {
            1: "января", 2: "февраля", 3: "марта", 4: "апреля",
            5: "мая", 6: "июня", 7: "июля", 8: "августа",
            9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
        }

        self._currency_symbols = {
            'ruble': '₽',
            'tenge': '₸',
            'dram': '֏',
            'som': 'Soʻm'
        }

        self._ascii_symbols = {
            # Математические
            'plus': '+', 'minus': '-', 'multiply': '*', 'divide': '/',
            'equals': '=', 'not_equal': '≠', 'less_equal': '≤', 'greater_equal': '≥',
            'approx': '≈', 'plus_minus': '±', 'infinity': '∞', 'pi': 'π', 'sum': '∑', 'integral': '∫',
            # Стрелки
            'arrow_left': '←', 'arrow_right': '→', 'arrow_up': '↑', 'arrow_down': '↓',
            'arrow_both': '↔', 'arrow_double_left': '«', 'arrow_double_right': '»',
            # Специальные
            'copyright': '©', 'registered': '®', 'trademark': '™', 'degree': '°',
            'section': '§', 'paragraph': '¶', 'bullet': '•', 'middle_dot': '·',
            'ellipsis': '…', 'em_dash': '—', 'en_dash': '–',
            # Кавычки
            'quote_left': '"', 'quote_right': '"', 'quote_single_left': "'", 'quote_single_right': "'",
            # Валюты
            'euro': '€', 'pound': '£', 'yen': '¥', 'cent': '¢',
            # Другие
            'check': '✓', 'cross': '✗', 'star': '★', 'heart': '♥',
            'diamond': '♦', 'club': '♣', 'spade': '♠'
        }

    def get_date_long(self) -> str:
        """Текущая дата в длинном формате"""
        now = datetime.now()
        return f"{now.day} {self._date_formats[now.month]} {now.year} года"

    def get_date_short(self) -> str:
        """Текущая дата в коротком формате"""
        return datetime.now().strftime("%d.%m.%Y")

    def get_datetime_full(self) -> str:
        """Дата и время"""
        return datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def get_time(self) -> str:
        """Текущее время"""
        return datetime.now().strftime("%H:%M:%S")

    def get_currency_symbol(self, currency: str) -> str:
        """Получить символ валюты"""
        return self._currency_symbols.get(currency.lower(), '')

    def get_ascii_symbol(self, symbol_name: str) -> str:
        """Получить ASCII символ"""
        return self._ascii_symbols.get(symbol_name.lower(), '')

    def insert_text(self, text: str) -> None:
        """Вставка текста с поддержкой русского языка и многострочности"""
        try:
            # Используем буфер обмена для русского текста
            original = pyperclip.paste()
            pyperclip.copy(text)
            keyboard.press_and_release('ctrl+v')
            time.sleep(0.05)
            pyperclip.copy(original)
        except ImportError:
            # Резервный метод для многострочного текста
            lines = text.split('\n')
            for i, line in enumerate(lines):
                keyboard.write(line)
                if i < len(lines) - 1:
                    keyboard.press_and_release('enter')
                    time.sleep(0.05)

    def execute_action(self, action: str) -> None:
        """Выполнение действия"""
        if action == "date_long":
            self.insert_text(self.get_date_long())
        elif action == "date_short":
            self.insert_text(self.get_date_short())
        elif action == "datetime":
            self.insert_text(self.get_datetime_full())
        elif action == "time":
            self.insert_text(self.get_time())
        elif action.startswith('currency:'):
            currency = action.replace('currency:', '')
            symbol = self.get_currency_symbol(currency)
            if symbol:
                self.insert_text(symbol)
        elif action.startswith('symbol:'):
            symbol_name = action.replace('symbol:', '')
            symbol = self.get_ascii_symbol(symbol_name)
            if symbol:
                self.insert_text(symbol)
        elif action.startswith('"') and action.endswith('"'):
            text = action[1:-1]
            self.insert_text(text)
        elif action.startswith('"""') and action.endswith('"""'):
            text = action[3:-3]
            self.insert_text(text)
        else:
            keyboard.send(action)