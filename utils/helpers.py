"""
Вспомогательные функции.
"""
import os
import shutil
from datetime import datetime
from typing import Optional
from constants import CONFIG_FILE, BACKUP_DIR


def create_backup() -> Optional[str]:
    """
    Создает резервную копию конфигурации.

    Returns:
        Путь к созданной резервной копии или None при ошибке
    """
    if not os.path.exists(CONFIG_FILE):
        return None

    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_DIR, f"config_backup_{timestamp}.json")
        shutil.copy2(CONFIG_FILE, backup_file)
        return backup_file
    except Exception as e:
        print(f"⚠️  Не удалось создать резервную копию: {e}")
        return None


def clear_screen():
    """Очищает экран консоли (кроссплатформенный)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def ensure_directory_exists(directory: str):
    """
    Создает директорию если она не существует.

    Args:
        directory: Путь к директории
    """
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def get_file_size(file_path: str) -> int:
    """
    Получает размер файла в байтах.

    Args:
        file_path: Путь к файлу

    Returns:
        Размер файла в байтах или -1 при ошибке
    """
    try:
        return os.path.getsize(file_path)
    except OSError:
        return -1


def format_file_size(size_bytes: int) -> str:
    """
    Форматирует размер файла в читаемый вид.

    Args:
        size_bytes: Размер в байтах

    Returns:
        Отформатированная строка размера
    """
    if size_bytes < 0:
        return "Неизвестно"

    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0

    return f"{size_bytes:.1f} TB"