"""
Модель настроек приложения.
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AppSettings:
    """Настройки приложения."""

    # Основные настройки
    auto_start: bool = False
    start_minimized: bool = False
    check_for_updates: bool = True

    # Настройки производительности
    typing_delay: float = 0.01
    clipboard_timeout: float = 0.05
    process_check_frequency: float = 0.1

    # Настройки резервного копирования
    auto_backup: bool = True
    max_backup_files: int = 10
    backup_on_start: bool = True

    # Настройки интерфейса
    show_notifications: bool = True
    compact_mode: bool = False
    theme: str = "default"

    # Расширенные настройки
    debug_mode: bool = False
    log_level: str = "INFO"

    def to_dict(self) -> Dict[str, Any]:
        """Сериализует настройки в словарь."""
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppSettings':
        """Создает настройки из словаря."""
        settings = cls()
        for key, value in data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        return settings