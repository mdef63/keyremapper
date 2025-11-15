"""
Главный файл приложения переназначения клавиш.
"""

import sys
import os
import traceback

# Добавляем путь для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Проверка обязательных зависимостей."""
    try:
        import keyboard
        print("✅ Библиотека 'keyboard' загружена")
    except ImportError:
        print("❌ Библиотека 'keyboard' не установлена!")
        print("💡 Установите: pip install keyboard")
        return False

    try:
        import pyperclip
        print("✅ Библиотека 'pyperclip' загружена")
    except ImportError:
        print("⚠️  Библиотека 'pyperclip' не установлена")
        print("💡 Для русского текста установите: pip install pyperclip")
        print("📝 Продолжаем с ограниченной функциональностью...")

    return True

def setup_directories():
    """Создание необходимых директорий."""
    try:
        os.makedirs("backups", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        print("✅ Директории созданы")
    except Exception as e:
        print(f"⚠️  Ошибка создания директорий: {e}")

def main():
    """Главная функция приложения."""
    print("🎹 Загрузка программы переназначения клавиш...")

    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)

    # Создаем директории
    setup_directories()

    try:
        from core.remapper import KeyboardRemapper
        from ui.menus import main_menu

        print("🔄 Инициализация ремаппера...")
        remapper = KeyboardRemapper()

        # Создаем начальную резервную копию если включено
        try:
            if hasattr(remapper, 'create_backup_with_description'):
                if remapper.create_backup_with_description("initial_backup"):
                    print("✅ Начальная резервная копия создана")
        except Exception as e:
            print(f"⚠️  Не удалось создать резервную копию: {e}")

        print("✅ Приложение готово к работе!")
        main_menu(remapper)

    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("💡 Проверьте структуру файлов и импорты")
        traceback.print_exc()
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        traceback.print_exc()
        print("\n💡 Попробуйте удалить файл конфигурации и перезапустить приложение")
        if os.path.exists("key_config.json"):
            print("💡 Файл конфигурации: key_config.json")


if __name__ == "__main__":
    main()