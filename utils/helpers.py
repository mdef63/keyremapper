"""
Вспомогательные функции для приложения переназначения клавиш.
"""

import os
import time
from typing import Optional

from constants import SYMBOL_CATEGORIES, CURRENCIES


def clear_screen():
    """Очищает экран (кроссплатформенный)"""
    os.system('cls' if os.name == 'nt' else 'clear')


def input_multiline_text() -> Optional[str]:
    """Ввод многострочного текста."""
    print("\n📝 Введите многострочный текст:")
    print("💡 Вводите строки текста. Для завершения введите 'END' на отдельной строке.")
    print("💡 Для ввода пустой строки просто нажмите Enter.")

    lines = []
    line_number = 1

    while True:
        line = input(f"Строка {line_number} (или 'END' для завершения): ")
        if line.upper() == 'END':
            break
        lines.append(line)
        line_number += 1

    return '\n'.join(lines) if lines else None


def select_symbol_from_category() -> Optional[str]:
    """Интерактивный выбор символа из категории."""
    print("\n🔣 Выберите категорию символов:")
    for cat_id, cat_info in SYMBOL_CATEGORIES.items():
        print(f"{cat_id}. {cat_info['name']} {cat_info['description']}")

    symbol_category = input("Ваш выбор (1-6): ").strip()
    if symbol_category not in SYMBOL_CATEGORIES:
        return None

    category = SYMBOL_CATEGORIES[symbol_category]
    print(f"\n{category['name']} символы:")

    for i, (symbol_id, symbol_char, symbol_desc) in enumerate(category['symbols'], 1):
        print(f"{i}. {symbol_char} {symbol_desc}")

    try:
        symbol_choice = int(input(f"Ваш выбор (1-{len(category['symbols'])}): ").strip())
        if 1 <= symbol_choice <= len(category['symbols']):
            return category['symbols'][symbol_choice - 1][0]
    except ValueError:
        pass

    return None


def select_currency() -> Optional[str]:
    """Интерактивный выбор валюты."""
    print("\n💱 Выберите валюту:")
    for i, (curr_id, curr_char, curr_name) in enumerate(CURRENCIES, 1):
        print(f"{i}. {curr_char} {curr_name}")

    try:
        choice = int(input("Ваш выбор (1-4): ").strip())
        if 1 <= choice <= len(CURRENCIES):
            return CURRENCIES[choice - 1][0]
        else:
            print("❌ Неверный номер")
    except ValueError:
        print("❌ Введите число")

    return None