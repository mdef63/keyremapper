"""
Модели данных для профилей и назначений клавиш.
"""
import copy
from typing import Dict, Any, Optional
from datetime import datetime


class KeyMapping:
    """Класс для представления назначения клавиши."""

    def __init__(self, key: str, action: str):
        self.key = key
        self.action = action

    def to_dict(self) -> Dict[str, str]:
        """Преобразует назначение в словарь."""
        return {'key': self.key, 'action': self.action}

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'KeyMapping':
        """Создает назначение из словаря."""
        return cls(data['key'], data['action'])

    def __eq__(self, other):
        if not isinstance(other, KeyMapping):
            return False
        return self.key == other.key and self.action == other.action

    def __repr__(self):
        return f"KeyMapping(key='{self.key}', action='{self.action}')"


class Profile:
    """Класс для представления профиля настроек."""

    def __init__(self, name: str, target_process: str = None):
        self.name = name
        self.target_process = target_process or "Yandex"
        self.mappings: Dict[str, str] = {}  # key -> action
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_mapping(self, key: str, action: str) -> bool:
        """
        Добавляет назначение клавиши.

        Args:
            key: Клавиша или комбинация
            action: Действие

        Returns:
            True если назначение добавлено, False если перезаписано существующее
        """
        is_new = key not in self.mappings
        self.mappings[key] = action
        self.updated_at = datetime.now()
        return is_new

    def remove_mapping(self, key: str) -> bool:
        """
        Удаляет назначение клавиши.

        Args:
            key: Клавиша для удаления

        Returns:
            True если назначение было удалено, False если не найдено
        """
        if key in self.mappings:
            del self.mappings[key]
            self.updated_at = datetime.now()
            return True
        return False

    def get_mapping(self, key: str) -> Optional[str]:
        """Получает действие для клавиши."""
        return self.mappings.get(key)

    def has_mapping(self, key: str) -> bool:
        """Проверяет наличие назначения для клавиши."""
        return key in self.mappings

    def clear_mappings(self):
        """Очищает все назначения."""
        self.mappings.clear()
        self.updated_at = datetime.now()

    def get_mappings_count(self) -> int:
        """Возвращает количество назначений."""
        return len(self.mappings)

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует профиль в словарь."""
        return {
            'mappings': copy.deepcopy(self.mappings),
            'target_process': self.target_process,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, name: str, data: Dict[str, Any]) -> 'Profile':
        """Создает профиль из словаря."""
        profile = cls(name)
        profile.mappings = data.get('mappings', {})
        profile.target_process = data.get('target_process', "Yandex")

        # Восстанавливаем даты если есть
        if 'created_at' in data:
            profile.created_at = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data:
            profile.updated_at = datetime.fromisoformat(data['updated_at'])

        return profile

    def __eq__(self, other):
        if not isinstance(other, Profile):
            return False
        return (self.name == other.name and
                self.target_process == other.target_process and
                self.mappings == other.mappings)

    def __repr__(self):
        return f"Profile(name='{self.name}', mappings={len(self.mappings)}, target='{self.target_process}')"