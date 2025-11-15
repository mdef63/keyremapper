"""
Валидаторы ввода для приложения переназначения клавиш.
"""

from typing import Optional, Callable


def validate_key(key: str) -> Optional[str]:
    """Проверка валидности клавиши."""
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
    special_keys = [
        'space', 'enter', 'tab', 'backspace', 'delete', 'esc', 'escape',
        'up', 'down', 'left', 'right', 'home', 'end', 'page up', 'page down',
        'insert', 'print screen', 'scroll lock', 'pause', 'caps lock',
        'num lock', 'num 0', 'num 1', 'num 2', 'num 3', 'num 4', 'num 5',
        'num 6', 'num 7', 'num 8', 'num 9', 'num +', 'num -', 'num *', 'num /', 'num enter',
        'shift', 'ctrl', 'alt', 'win', 'menu'
    ]
    if key_lower in special_keys:
        return key_lower

    # Комбинации клавиш
    parts = [p.strip() for p in key_lower.split('+')]
    if len(parts) >= 2:
        modifiers = ['ctrl', 'alt', 'shift', 'win']
        if all(part in modifiers for part in parts[:-1]):
            main_key = parts[-1]
            if validate_key(main_key):
                return key_lower

    return None


def safe_input(prompt: str, default: Optional[str] = None,
              validator: Optional[Callable[[str], bool]] = None) -> Optional[str]:
    """Безопасный ввод с валидацией."""
    while True:
        try:
            value = input(prompt).strip()
            if not value and default is not None:
                return default
            if validator and not validator(value):
                print("❌ Неверное значение, попробуйте снова")
                continue
            return value
        except (EOFError, KeyboardInterrupt):
            print("\n❌ Отменено")
            return None