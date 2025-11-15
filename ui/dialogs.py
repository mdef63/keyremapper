"""
Диалоги и интерактивные меню для пользовательского ввода.
"""
from typing import Optional, List, Tuple
from constants import SYMBOL_CATEGORIES, CURRENCIES
from utils.validators import InputValidator


class Dialogs:
    """Класс для управления диалогами и пользовательским вводом."""

    @staticmethod
    def select_symbol_from_category() -> Optional[str]:
        """
        Интерактивный выбор символа из категории.

        Returns:
            ID выбранного символа или None если отменено
        """
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

        symbol_choice = input(f"Ваш выбор (1-{len(category['symbols'])}): ").strip()

        try:
            choice_num = int(symbol_choice)
            if 1 <= choice_num <= len(category['symbols']):
                return category['symbols'][choice_num - 1][0]  # Возвращаем symbol_id
        except ValueError:
            pass

        return None

    @staticmethod
    def select_currency() -> Optional[str]:
        """
        Интерактивный выбор валюты.

        Returns:
            ID выбранной валюты или None если отменено
        """
        print("\n💱 Выберите валюту:")
        for i, (curr_id, curr_char, curr_name) in enumerate(CURRENCIES, 1):
            print(f"{i}. {curr_char} {curr_name}")

        choice = input("Ваш выбор (1-4): ").strip()
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(CURRENCIES):
                return CURRENCIES[choice_num - 1][0]  # Возвращаем currency_id
            else:
                print("❌ Неверный номер")
        except ValueError:
            print("❌ Введите число")

        return None

    @staticmethod
    def input_multiline_text() -> Optional[str]:
        """
        Ввод многострочного текста с поддержкой пустых строк и завершением через END.

        Returns:
            Многострочный текст или None если отменено
        """
        print("\n📝 Введите многострочный текст:")
        print("💡 Вводите строки текста. Для завершения введите 'END' на отдельной строке.")
        print("💡 Для ввода пустой строки просто нажмите Enter.")

        lines = []
        line_number = 1

        while True:
            try:
                line = input(f"Строка {line_number} (или 'END' для завершения): ")

                if line.upper() == 'END':
                    break

                lines.append(line)
                line_number += 1

            except (EOFError, KeyboardInterrupt):
                print("\n❌ Отменено")
                return None

        if lines:
            multiline_text = '\n'.join(lines)
            print(f"✅ Текст сохранен ({len(lines)} строк)")
            return multiline_text
        else:
            print("❌ Текст не может быть пустым")
            return None

    @staticmethod
    def select_from_list(items: List[Tuple[str, str]], title: str,
                        prompt: str) -> Optional[str]:
        """
        Выбор элемента из списка.

        Args:
            items: Список элементов (value, display_text)
            title: Заголовок меню
            prompt: Подсказка для ввода

        Returns:
            Выбранное значение или None если отменено
        """
        if not items:
            print("❌ Нет доступных элементов")
            return None

        print(f"\n{title}:")
        for i, (value, display) in enumerate(items, 1):
            print(f"{i}. {display}")

        try:
            choice = input(f"{prompt} (1-{len(items)}): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(items):
                return items[choice_num - 1][0]
            else:
                print("❌ Неверный номер")
        except ValueError:
            print("❌ Введите число")
        except (EOFError, KeyboardInterrupt):
            print("\n❌ Отменено")

        return None

    @staticmethod
    def confirm_action(message: str) -> bool:
        """
        Подтверждение действия пользователем.

        Args:
            message: Сообщение для подтверждения

        Returns:
            True если пользователь подтвердил, False если отменил
        """
        try:
            response = input(f"{message} (y/n): ").strip().lower()
            return response in ['y', 'yes', 'д', 'да']
        except (EOFError, KeyboardInterrupt):
            return False

    @staticmethod
    def input_with_validation(prompt: str, default: str = None,
                            validator: callable = None) -> Optional[str]:
        """
        Ввод с валидацией.

        Args:
            prompt: Подсказка для ввода
            default: Значение по умолчанию
            validator: Функция валидации

        Returns:
            Введенное значение или None если отменено
        """
        return InputValidator.safe_input(prompt, default, validator)