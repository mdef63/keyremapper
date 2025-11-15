"""
Модель профиля настроек.
"""

from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class Profile:
    """Профиль настроек переназначения клавиш."""

    name: str
    mappings: Dict[str, str] = field(default_factory=dict)
    target_process: str = "Yandex"

    def add_mapping(self, key: str, action: str) -> None:
        """Добавляет назначение клавиши."""
        self.mappings[key] = action

    def remove_mapping(self, key: str) -> None:
        """Удаляет назначение клавиши."""
        if key in self.mappings:
            del self.mappings[key]

    def get_mapping(self, key: str) -> str:
        """Возвращает действие для клавиши."""
        return self.mappings.get(key)

    def mapping_count(self) -> int:
        """Возвращает количество назначений."""
        return len(self.mappings)

    def to_dict(self) -> Dict[str, Any]:
        """Сериализует профиль в словарь."""
        return {
            'mappings': self.mappings,
            'target_process': self.target_process
        }

    @classmethod
    def from_dict(cls, name: str, data: Dict[str, Any]) -> 'Profile':
        """Создает профиль из словаря."""
        # Обрабатываем случай, когда data может быть None или не содержать ожидаемых ключей
        if not data:
            data = {}

        return cls(
            name=name,
            mappings=data.get('mappings', {}),
            target_process=data.get('target_process', 'Yandex')
        )