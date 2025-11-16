"""
Менеджер макросов для приложения переназначения клавиш.
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from models.mapping import Macro


class MacroManager:
    """Управление макросами."""

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.macros_file = Path("macros.json")
        self.macros: Dict[str, Macro] = {}
        self.load_macros()

    def load_macros(self) -> None:
        """Загружает макросы из файла."""
        try:
            if self.macros_file.exists():
                with open(self.macros_file, 'r', encoding='utf-8') as f:
                    macros_data = json.load(f)

                self.macros = {}
                for name, data in macros_data.items():
                    self.macros[name] = Macro(
                        name=name,
                        action_type=data.get('action_type', 'text'),
                        value=data.get('value', ''),
                        description=data.get('description', ''),
                        category=data.get('category', 'general')
                    )
            else:
                self.macros = {}
                self._create_default_macros()
        except Exception as e:
            print(f"❌ Ошибка загрузки макросов: {e}")
            self.macros = {}
            self._create_default_macros()

    def _create_default_macros(self) -> None:
        """Создает макросы по умолчанию."""
        default_macros = {
            'email_signature': Macro(
                name='email_signature',
                action_type='text',
                value='С уважением,\n[Ваше Имя]\n[Ваша Должность]',
                description='Подпись для email',
                category='text'
            ),
            'current_datetime': Macro(
                name='current_datetime',
                action_type='action',
                value='datetime',
                description='Текущие дата и время',
                category='datetime'
            ),
            'separator': Macro(
                name='separator',
                action_type='text',
                value='---',
                description='Разделитель',
                category='text'
            )
        }
        self.macros.update(default_macros)
        self.save_macros()

    def save_macros(self) -> bool:
        """Сохраняет макросы в файл."""
        try:
            macros_data = {}
            for name, macro in self.macros.items():
                macros_data[name] = {
                    'action_type': macro.action_type,
                    'value': macro.value,
                    'description': macro.description,
                    'category': macro.category
                }

            with open(self.macros_file, 'w', encoding='utf-8') as f:
                json.dump(macros_data, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения макросов: {e}")
            return False

    def create_macro(self, name: str, action_type: str, value: str,
                     description: str = "", category: str = "general") -> bool:
        """Создает новый макрос."""
        if name in self.macros:
            return False

        self.macros[name] = Macro(
            name=name,
            action_type=action_type,
            value=value,
            description=description,
            category=category
        )

        return self.save_macros()

    def delete_macro(self, name: str) -> bool:
        """Удаляет макрос."""
        if name not in self.macros:
            return False

        del self.macros[name]
        return self.save_macros()

    def get_macro(self, name: str) -> Optional[Macro]:
        """Возвращает макрос по имени."""
        return self.macros.get(name)

    def list_macros(self, category: str = None) -> List[Macro]:
        """Возвращает список макросов."""
        if category:
            return [macro for macro in self.macros.values() if macro.category == category]
        return list(self.macros.values())

    def get_categories(self) -> List[str]:
        """Возвращает список категорий макросов."""
        categories = set()
        for macro in self.macros.values():
            categories.add(macro.category)
        return sorted(categories)

    def execute_macro(self, name: str, executor) -> bool:
        """Выполняет макрос."""
        macro = self.get_macro(name)
        if not macro:
            return False

        try:
            macro.execute(executor)
            return True
        except Exception as e:
            print(f"❌ Ошибка выполнения макроса '{name}': {e}")
            return False

    def import_macros_from_mappings(self, mappings: Dict[str, str]) -> int:
        """Импортирует макросы из назначений."""
        imported_count = 0
        for key, action in mappings.items():
            macro_name = f"macro_{key}"
            if macro_name not in self.macros:
                if self.create_macro(
                        name=macro_name,
                        action_type='action',
                        value=action,
                        description=f"Макрос из назначения {key}",
                        category='imported'
                ):
                    imported_count += 1
        return imported_count