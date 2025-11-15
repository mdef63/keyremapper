"""
Валидаторы для проверки входных данных.
"""
import re
from typing import Optional, Callable
from constants import SPECIAL_KEYS, KEY_MODIFIERS


class KeyValidator:
    """Валидатор для проверки корректности клавиш."""

    @staticmethod
    def validate_key(key: str) -> Optional[str]:
        """
        Проверяет валидность клавиши или комбинации.

        Args:
            key: Клавиша для проверки

        Returns:
            Нормализованную клавишу если валидна, иначе None
        """
        if not key or not isinstance(key, str):
            return None

        key_lower = key.lower().strip()

        # Функциональные клавиши F1-F24
        if key_lower.startswith('f') and len(key_lower) > 1:
            try:
                num = int(key_lower[1:])
                if 1 <= num <= 24:
                    return key_lower
            except ValueError:
                pass

        # Буквы a-z
        if len(key_lower) == 1 and key_lower.isalpha():
            return key_lower

        # Цифры 0-9
        if len(key_lower) == 1 and key_lower.isdigit():
            return key_lower

        # Специальные клавиши
        if key_lower in SPECIAL_KEYS:
            return key_lower

        # Комбинации клавиш (например, ctrl+a, alt+f4)
        return KeyValidator._validate_key_combo(key_lower)

    @staticmethod
    def _validate_key_combo(key: str) -> Optional[str]:
        """
        Проверяет валидность комбинации клавиш.

        Args:
            key: Комбинация клавиш

        Returns:
            Нормализованную комбинацию если валидна, иначе None
        """
        parts = [p.strip() for p in key.split('+')]

        if len(parts) < 2:
            return None

        # Проверяем, что все части кроме последней - модификаторы
        for part in parts[:-1]:
            if part not in KEY_MODIFIERS:
                return None

        # Проверяем основную клавишу
        main_key = parts[-1]
        if KeyValidator.validate_key(main_key):
            return key

        return None

    @staticmethod
    def is_function_key(key: str) -> bool:
        """Проверяет, является ли клавиша функциональной (F1-F24)."""
        key_lower = key.lower()
        return key_lower.startswith('f') and len(key_lower) > 1 and key_lower[1:].isdigit()

    @staticmethod
    def is_key_combo(key: str) -> bool:
        """Проверяет, является ли клавиша комбинацией."""
        return '+' in key.lower()


class InputValidator:
    """Валидатор для пользовательского ввода."""

    @staticmethod
    def validate_profile_name(name: str) -> bool:
        """Проверяет валидность имени профиля."""
        if not name or not name.strip():
            return False
        # Запрещаем специальные символы в именах профилей
        return bool(re.match(r'^[a-zA-Z0-9_\- ]+$', name))

    @staticmethod
    def validate_process_name(name: str) -> bool:
        """Проверяет валидность имени процесса."""
        return bool(name and name.strip())

    @staticmethod
    def safe_input(prompt: str, default: str = None,
                   validator: Callable[[str], bool] = None) -> Optional[str]:
        """
        Безопасный ввод с валидацией.

        Args:
            prompt: Подсказка для ввода
            default: Значение по умолчанию
            validator: Функция валидации

        Returns:
            Введенное значение или None если отменено
        """
        while True:
            try:
                value = input(prompt).strip()

                if not value and default is not None:
                    return default

                if not value:
                    continue

                if validator and not validator(value):
                    print("❌ Неверное значение, попробуйте снова")
                    continue

                return value

            except (EOFError, KeyboardInterrupt):
                print("\n❌ Отменено")
                return None