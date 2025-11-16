"""
Скрипт для сборки проекта в EXE
"""

import os
import sys
import shutil
from pathlib import Path


def build_exe():
    """Собирает проект в EXE файл"""
    try:
        import PyInstaller.__main__

        # Параметры для PyInstaller
        params = [
            'main.py',  # Главный файл
            '--name=KeyboardRemapper',  # Имя исполняемого файла
            '--onefile',  # Собрать в один файл
            '--console',  # Консольное приложение
            '--icon=assets/icon.ico',  # Иконка (если есть)
            '--add-data=constants.py;.',  # Добавить константы
            '--add-data=core;core',  # Добавить папку core
            '--add-data=ui;ui',  # Добавить папку ui
            '--add-data=models;models',  # Добавить папку models
            '--add-data=utils;utils',  # Добавить папку utils
            '--hidden-import=win32gui',  # Явно указать скрытые импорты
            '--hidden-import=win32process',
            '--hidden-import=psutil',
            '--hidden-import=pyperclip',
            '--hidden-import=keyboard',
            '--clean',  # Очистить кэш
            '--noconfirm',  # Не спрашивать подтверждение
        ]

        print("🚀 Начинаем сборку EXE...")
        PyInstaller.__main__.run(params)
        print("✅ Сборка завершена успешно!")

    except ImportError:
        print("❌ PyInstaller не установлен!")
        print("💡 Установите: pip install pyinstaller")
        return False
    except Exception as e:
        print(f"❌ Ошибка при сборке: {e}")
        return False

    return True


def cleanup():
    """Очистка временных файлов"""
    temp_dirs = ['build', '__pycache__']
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🧹 Удалена папка: {temp_dir}")


if __name__ == "__main__":
    if build_exe():
        cleanup()
        print("\n🎉 Готово! EXE файл находится в папке 'dist'")
        print("📁 dist/KeyboardRemapper.exe")
    else:
        print("\n❌ Сборка не удалась!")