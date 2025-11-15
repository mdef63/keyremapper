"""
Модели для работы с назначениями клавиш.
"""
from typing import Dict, List, Tuple, Optional
from enum import Enum


class ActionType(Enum):
    """Типы действий для назначений клавиш."""
    TEXT = "text"
    MULTILINE_TEXT = "multiline_text"
    DATE_LONG = "date_long"
    DATE_SHORT = "date_short"
    DATETIME = "datetime"
    TIME = "time"
    CURRENCY = "currency"
    SYMBOL = "symbol"
    KEY_COMBO = "key_combo"


class MappingManager:
    """Менеджер для работы с назначениями клавиш."""

    def __init__(self):
        self.mappings: Dict[str, str] = {}

    def add(self, key: str, action: str) -> bool:
        """
        Добавляет новое назначение.

        Args:
            key: Клавиша или комбинация
            action: Действие

        Returns:
            True если добавлено, False если перезаписано существующее
        """
        existed = key in self.mappings
        self.mappings[key] = action
        return not existed

    def remove(self, key: str) -> bool:
        """
        Удаляет назначение.

        Args:
            key: Клавиша для удаления

        Returns:
            True если удалено, False если не найдено
        """
        if key in self.mappings:
            del self.mappings[key]
            return True
        return False

    def get(self, key: str) -> Optional[str]:
        """Получает действие для клавиши."""
        return self.mappings.get(key)

    def exists(self, key: str) -> bool:
        """Проверяет наличие назначения."""
        return key in self.mappings

    def clear(self):
        """Очищает все назначения."""
        self.mappings.clear()

    def count(self) -> int:
        """Возвращает количество назначений."""
        return len(self.mappings)

    def get_all(self) -> List[Tuple[str, str]]:
        """Возвращает все назначения в виде списка кортежей (key, action)."""
        return list(self.mappings.items())

    def search(self, search_term: str) -> List[Tuple[str, str]]:
        """
        Ищет назначения по поисковому запросу.

        Args:
            search_term: Поисковый запрос

        Returns:
            Список найденных назначений (key, action)
        """
        if not search_term:
            return []

        search_terms = search_term.lower().split()
        results = []

        for key, action in self.mappings.items():
            search_text = f"{key} {action}".lower()
            if all(term in search_text for term in search_terms):
                results.append((key, action))

        return results

    def to_dict(self) -> Dict[str, str]:
        """Преобразует назначения в словарь."""
        return self.mappings.copy()

    def from_dict(self, mappings_dict: Dict[str, str]):
        """Загружает назначения из словаря."""
        self.mappings = mappings_dict.copy()