"""
Исполнитель действий для назначений клавиш.
"""
import time
from datetime import datetime
from typing import Optional
from constants import CURRENCY_SYMBOLS, ASCII_SYMBOLS, MONTHS


class ActionExecutor:
    """Исполнитель действий для назначений клавиш."""

    def __init__(self):
        self._clipboard_available = self._check_clipboard_availability()

    def _check_clipboard_availability(self) -> bool:
        """Проверяет доступность буфера обмена."""
        try:
            import pyperclip
            return True
        except ImportError:
            return False

    def execute_action(self, action: str):
        """
        Выполняет действие назначения клавиши.

        Args:
            action: Действие для выполнения
        """
        if not action:
            return

        try:
            if action == "date_long":
                self._insert_text(self._get_date_long())
            elif action == "date_short":
                self._insert_text(self._get_date_short())
            elif action == "datetime":
                self._insert_text(self._get_datetime_full())
            elif action == "time":
                self._insert_text(self._get_time())
            elif action.startswith('currency:'):
                self._handle_currency_action(action)
            elif action.startswith('symbol:'):
                self._handle_symbol_action(action)
            elif action.startswith('"') and action.endswith('"'):
                self._handle_text_action(action)
            elif action.startswith('"""') and action.endswith('"""'):
                self._handle_multiline_action(action)
            else:
                self._handle_key_combo(action)

        except Exception as e:
            print(f"❌ Ошибка при выполнении действия: {e}")

    def _get_date_long(self) -> str:
        """Получает текущую дату в длинном формате."""
        now = datetime.now()
        return f"{now.day} {MONTHS[now.month]} {now.year} года"

    def _get_date_short(self) -> str:
        """Получает текущую дату в коротком формате."""
        return datetime.now().strftime("%d.%m.%Y")

    def _get_datetime_full(self) -> str:
        """Получает дату и время."""
        return datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def _get_time(self) -> str:
        """Получает текущее время."""
        return datetime.now().strftime("%H:%M:%S")

    def _get_currency_symbol(self, currency: str) -> str:
        """Получает символ валюты."""
        return CURRENCY_SYMBOLS.get(currency.lower(), '')

    def _get_ascii_symbol(self, symbol_name: str) -> str:
        """Получает ASCII символ."""
        return ASCII_SYMBOLS.get(symbol_name.lower(), '')

    def _handle_currency_action(self, action: str):
        """Обрабатывает действие вставки символа валюты."""
        currency = action.replace('currency:', '')
        symbol = self._get_currency_symbol(currency)
        if symbol:
            self._insert_text(symbol)

    def _handle_symbol_action(self, action: str):
        """Обрабатывает действие вставки ASCII символа."""
        symbol_name = action.replace('symbol:', '')
        symbol = self._get_ascii_symbol(symbol_name)
        if symbol:
            self._insert_text(symbol)

    def _handle_text_action(self, action: str):
        """Обрабатывает действие вставки текста (одна строка)."""
        text = action[1:-1]
        self._insert_text(text)

    def _handle_multiline_action(self, action: str):
        """Обрабатывает действие вставки многострочного текста."""
        text = action[3:-3]
        self._insert_text(text)

    def _handle_key_combo(self, action: str):
        """Обрабатывает действие отправки комбинации клавиш."""
        import keyboard
        keyboard.send(action)

    def _insert_text(self, text: str):
        """
        Вставляет текст с поддержкой русского языка и многострочности.

        Args:
            text: Текст для вставки
        """
        if not text:
            return

        try:
            if self._clipboard_available:
                self._insert_via_clipboard(text)
            else:
                self._insert_via_keyboard(text)
        except Exception as e:
            print(f"❌ Ошибка при вставке текста: {e}")

    def _insert_via_clipboard(self, text: str):
        """Вставляет текст через буфер обмена."""
        import pyperclip
        import keyboard

        original = pyperclip.paste()
        pyperclip.copy(text)
        keyboard.press_and_release('ctrl+v')
        time.sleep(0.05)  # Даем время для вставки
        pyperclip.copy(original)

    def _insert_via_keyboard(self, text: str):
        """Вставляет текст через эмуляцию клавиатуры."""
        import keyboard

        lines = text.split('\n')
        for i, line in enumerate(lines):
            keyboard.write(line)
            if i < len(lines) - 1:  # Не нажимаем Enter после последней строки
                keyboard.press_and_release('enter')
                time.sleep(0.05)