"""
Модель назначения клавиш.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class ActionType(Enum):
    """Типы поддерживаемых действий."""
    TEXT = "text"
    MULTILINE_TEXT = "multiline_text"
    DATE_LONG = "date_long"
    DATE_SHORT = "date_short"
    DATETIME = "datetime"
    TIME = "time"
    CURRENCY = "currency"
    SYMBOL = "symbol"
    KEY_COMBO = "key_combo"
    MACRO = "macro"


@dataclass
class KeyMapping:
    """Назначение клавиши."""

    key: str
    action: str
    action_type: ActionType

    def get_display_info(self) -> tuple:
        """Возвращает отображаемую информацию о маппинге."""
        from utils.formatters import format_key_display, get_action_display
        return format_key_display(self.key), get_action_display(self.action)


@dataclass
class Macro:
    """Макрос - предопределенное действие."""

    name: str
    action_type: str  # text, action, key_combo
    value: str
    description: str = ""
    category: str = "general"

    def execute(self, executor) -> None:
        """Выполняет макрос."""
        if self.action_type == "text":
            executor.insert_text(self.value)
        elif self.action_type == "action":
            executor.execute_action(self.value)
        elif self.action_type == "key_combo":
            import keyboard
            keyboard.send(self.value)