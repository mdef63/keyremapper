"""
Главный файл приложения для переназначения клавиш.
"""
import sys
import os

# Добавляем корневую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.remapper import KeyboardRemapper
from ui.menus import MenuManager
from constants import WINDOWS_API_AVAILABLE


def check_dependencies():
    """Проверяет необходимые зависимости."""
    try:
        import keyboard
    except ImportError:
        print("❌ Библиотека 'keyboard' не установлена!")
        print("💡 Установите: pip install keyboard")
        return False

    try:
        import pyperclip
    except ImportError:
        print("⚠️  Библиотека 'pyperclip' не установлена")
        print("💡 Для русского текста установите: pip install pyperclip")
        print("📝 Продолжаем с ограниченной функциональностью...")

    if not WINDOWS_API_AVAILABLE:
        print("⚠️  Библиотеки для определения процесса не установлены")
        print("💡 Для работы с процессами установите: pip install pywin32 psutil")
        print("📝 Переназначение будет работать для всех окон...")

    return True


def main():
    """Главная функция приложения."""
    print("🎹 Загрузка программы переназначения клавиш...")

    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)

    try:
        # Инициализируем ремаппер
        remapper = KeyboardRemapper()

        # Инициализируем менеджер меню
        menu_manager = MenuManager(remapper)

        # Запускаем главное меню
        menu_manager.show_menu('main')

    except KeyboardInterrupt:
        print("\n\n👋 До свидания!")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        print("💡 Проверьте настройки и попробуйте снова")
        input("Нажмите Enter для выхода...")


if __name__ == "__main__":
    main()