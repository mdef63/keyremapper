"""
Управление конфигурацией приложения.
"""

import os
import shutil
import json
from datetime import datetime
from typing import Dict, Any, Optional

from constants import CONFIG_FILE, BACKUP_DIR, DEFAULT_PROFILE, DEFAULT_TARGET_PROCESS
from models.profile import Profile


class ConfigManager:
    """Управление конфигурацией приложения."""

    def __init__(self):
        self.profiles: Dict[str, Profile] = {}
        self.current_profile_name: str = DEFAULT_PROFILE
        self._ensure_default_profile()

    def _ensure_default_profile(self) -> None:
        """Убеждается, что профиль по умолчанию существует."""
        if DEFAULT_PROFILE not in self.profiles:
            self.profiles[DEFAULT_PROFILE] = Profile(
                name=DEFAULT_PROFILE,
                mappings={},
                target_process=DEFAULT_TARGET_PROCESS
            )

    def create_backup(self) -> Optional[str]:
        """Создает резервную копию конфигурации."""
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

    def load_config(self) -> bool:
        """Загружает конфигурацию из файла."""
        if not os.path.exists(CONFIG_FILE):
            self._initialize_default_config()
            return False

        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Обработка разных форматов конфигурации
            if isinstance(config, dict) and 'profiles' in config:
                # Новый формат с профилями
                self.profiles = {}
                for profile_name, profile_data in config['profiles'].items():
                    self.profiles[profile_name] = Profile.from_dict(profile_name, profile_data)
                self.current_profile_name = config.get('current_profile', DEFAULT_PROFILE)
            elif isinstance(config, dict) and 'mappings' in config:
                # Старый формат (без профилей) - мигрируем в профиль default
                self.profiles = {
                    DEFAULT_PROFILE: Profile.from_dict(DEFAULT_PROFILE, {
                        'mappings': config.get('mappings', {}),
                        'target_process': config.get('target_process', DEFAULT_TARGET_PROCESS)
                    })
                }
                self.current_profile_name = DEFAULT_PROFILE
            else:
                # Очень старый формат - только mappings
                self.profiles = {
                    DEFAULT_PROFILE: Profile.from_dict(DEFAULT_PROFILE, {
                        'mappings': config,
                        'target_process': DEFAULT_TARGET_PROCESS
                    })
                }
                self.current_profile_name = DEFAULT_PROFILE

            # Убеждаемся, что есть профиль по умолчанию
            self._ensure_default_profile()

            # Проверяем, что текущий профиль существует
            if self.current_profile_name not in self.profiles:
                print(f"⚠️  Профиль '{self.current_profile_name}' не найден, переключаемся на '{DEFAULT_PROFILE}'")
                self.current_profile_name = DEFAULT_PROFILE

            print(f"✅ Конфигурация загружена (профиль: {self.current_profile_name})")
            return True
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            self._initialize_default_config()
            return False

    def _initialize_default_config(self) -> None:
        """Инициализация конфигурации по умолчанию."""
        self.profiles = {
            DEFAULT_PROFILE: Profile(
                name=DEFAULT_PROFILE,
                mappings={},
                target_process=DEFAULT_TARGET_PROCESS
            )
        }
        self.current_profile_name = DEFAULT_PROFILE
        print("📝 Создана конфигурация по умолчанию")

    def save_config(self, create_backup: bool = True) -> bool:
        """Сохранение конфигурации в файл."""
        try:
            # Убеждаемся, что профиль по умолчанию существует перед сохранением
            self._ensure_default_profile()

            if create_backup and os.path.exists(CONFIG_FILE):
                self.create_backup()

            config = {
                'profiles': {name: profile.to_dict() for name, profile in self.profiles.items()},
                'current_profile': self.current_profile_name
            }

            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return False

    def get_current_profile(self) -> Profile:
        """Возвращает текущий профиль."""
        # Убеждаемся, что текущий профиль существует
        if self.current_profile_name not in self.profiles:
            print(f"⚠️  Профиль '{self.current_profile_name}' не найден, используем '{DEFAULT_PROFILE}'")
            self.current_profile_name = DEFAULT_PROFILE
            self._ensure_default_profile()

        return self.profiles[self.current_profile_name]

    def set_current_profile(self, profile_name: str) -> bool:
        """Устанавливает текущий профиль."""
        if profile_name in self.profiles:
            self.current_profile_name = profile_name
            return True

        print(f"❌ Профиль '{profile_name}' не найден")
        return False

    def add_profile(self, profile: Profile) -> bool:
        """Добавляет профиль."""
        if profile.name in self.profiles:
            return False
        self.profiles[profile.name] = profile
        return True

    def remove_profile(self, profile_name: str) -> bool:
        """Удаляет профиль."""
        if profile_name == DEFAULT_PROFILE:
            print("❌ Нельзя удалить профиль по умолчанию")
            return False

        if profile_name in self.profiles:
            # Если удаляем текущий профиль, переключаемся на default
            if profile_name == self.current_profile_name:
                self.current_profile_name = DEFAULT_PROFILE
                self._ensure_default_profile()

            del self.profiles[profile_name]
            return True

        return False

    def get_profile_names(self) -> list:
        """Возвращает список имен профилей."""
        return list(self.profiles.keys())

    def list_profiles(self) -> None:
        """Показать список всех профилей."""
        if not self.profiles:
            print("📝 Нет профилей")
            return

        print(f"\n📋 Профили (текущий: {self.current_profile_name}):")
        for profile_name in sorted(self.profiles.keys()):
            profile = self.profiles[profile_name]
            mappings_count = len(profile.mappings)
            target_process = profile.target_process
            marker = "👉" if profile_name == self.current_profile_name else "  "
            print(f"{marker} {profile_name} - {mappings_count} назначений, процесс: {target_process}")