"""
Управление конфигурацией приложения.
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from models.profile import Profile
from utils.helpers import create_backup
from constants import CONFIG_FILE, DEFAULT_PROFILE


class ConfigManager:
    """Менеджер конфигурации приложения."""

    def __init__(self):
        self.profiles: Dict[str, Profile] = {}
        self.current_profile_name = DEFAULT_PROFILE
        self.config_file = CONFIG_FILE

    def load_config(self) -> bool:
        """
        Загружает конфигурацию из файла.

        Returns:
            True если загрузка успешна, False при ошибке
        """
        if not os.path.exists(self.config_file):
            self._create_default_config()
            return True

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            return self._parse_config_data(config_data)

        except Exception as e:
            print(f"❌ Ошибка загрузки конфигурации: {e}")
            self._create_default_config()
            return False

    def _parse_config_data(self, config_data: Dict[str, Any]) -> bool:
        """
        Парсит данные конфигурации.

        Args:
            config_data: Данные конфигурации

        Returns:
            True если парсинг успешен
        """
        try:
            # Новый формат с профилями
            if 'profiles' in config_data:
                self.profiles = {}
                self.current_profile_name = config_data.get('current_profile', DEFAULT_PROFILE)

                # Загружаем профили
                for profile_name, profile_data in config_data['profiles'].items():
                    self.profiles[profile_name] = Profile.from_dict(profile_name, profile_data)

                # Создаем профиль по умолчанию если его нет
                if DEFAULT_PROFILE not in self.profiles:
                    self.profiles[DEFAULT_PROFILE] = Profile(DEFAULT_PROFILE)

                # Проверяем текущий профиль
                if self.current_profile_name not in self.profiles:
                    self.current_profile_name = DEFAULT_PROFILE

            elif 'mappings' in config_data:
                # Миграция старого формата
                self._migrate_old_format(config_data)
            else:
                # Очень старый формат
                self._create_default_config()

            print(f"✅ Конфигурация загружена (профиль: {self.current_profile_name})")
            return True

        except Exception as e:
            print(f"❌ Ошибка парсинга конфигурации: {e}")
            self._create_default_config()
            return False

    def _migrate_old_format(self, config_data: Dict[str, Any]):
        """Мигрирует старый формат конфигурации в новый."""
        print("🔄 Миграция старого формата конфигурации...")

        profile = Profile(DEFAULT_PROFILE)
        profile.mappings = config_data.get('mappings', {})
        profile.target_process = config_data.get('target_process', 'Yandex')

        self.profiles = {DEFAULT_PROFILE: profile}
        self.current_profile_name = DEFAULT_PROFILE

    def _create_default_config(self):
        """Создает конфигурацию по умолчанию."""
        self.profiles = {DEFAULT_PROFILE: Profile(DEFAULT_PROFILE)}
        self.current_profile_name = DEFAULT_PROFILE
        print("📝 Создана конфигурация по умолчанию")

    def save_config(self, create_backup_file: bool = True) -> bool:
        """
        Сохраняет конфигурацию в файл.

        Args:
            create_backup_file: Создавать ли резервную копию

        Returns:
            True если сохранение успешно, False при ошибке
        """
        try:
            # Создаем резервную копию
            if create_backup_file and os.path.exists(self.config_file):
                create_backup()

            # Подготавливаем данные для сохранения
            config_data = {
                'profiles': {name: profile.to_dict() for name, profile in self.profiles.items()},
                'current_profile': self.current_profile_name,
                'saved_at': datetime.now().isoformat()
            }

            # Сохраняем
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)

            print("✅ Конфигурация сохранена")
            return True

        except Exception as e:
            print(f"❌ Ошибка сохранения конфигурации: {e}")
            return False

    def get_current_profile(self) -> Optional[Profile]:
        """Получает текущий профиль."""
        return self.profiles.get(self.current_profile_name)

    def set_current_profile(self, profile_name: str) -> bool:
        """
        Устанавливает текущий профиль.

        Args:
            profile_name: Имя профиля

        Returns:
            True если профиль установлен, False если не найден
        """
        if profile_name in self.profiles:
            self.current_profile_name = profile_name
            return True
        return False

    def create_profile(self, name: str, copy_from: str = None) -> bool:
        """
        Создает новый профиль.

        Args:
            name: Имя нового профиля
            copy_from: Имя профиля для копирования настроек

        Returns:
            True если профиль создан, False если уже существует
        """
        if name in self.profiles:
            return False

        new_profile = Profile(name)

        # Копируем настройки если указано
        if copy_from and copy_from in self.profiles:
            source_profile = self.profiles[copy_from]
            new_profile.mappings = source_profile.mappings.copy()
            new_profile.target_process = source_profile.target_process

        self.profiles[name] = new_profile
        return True

    def delete_profile(self, name: str) -> bool:
        """
        Удаляет профиль.

        Args:
            name: Имя профиля для удаления

        Returns:
            True если профиль удален, False если не найден или это последний профиль
        """
        if name not in self.profiles or len(self.profiles) <= 1:
            return False

        # Нельзя удалить текущий профиль
        if name == self.current_profile_name:
            return False

        del self.profiles[name]
        return True

    def rename_profile(self, old_name: str, new_name: str) -> bool:
        """
        Переименовывает профиль.

        Args:
            old_name: Текущее имя профиля
            new_name: Новое имя профиля

        Returns:
            True если профиль переименован, False при ошибке
        """
        if (old_name not in self.profiles or
            new_name in self.profiles or
            not new_name.strip()):
            return False

        profile = self.profiles[old_name]
        del self.profiles[old_name]

        # Создаем профиль с новым именем
        renamed_profile = Profile(new_name)
        renamed_profile.mappings = profile.mappings.copy()
        renamed_profile.target_process = profile.target_process
        renamed_profile.created_at = profile.created_at
        renamed_profile.updated_at = datetime.now()

        self.profiles[new_name] = renamed_profile

        # Обновляем текущий профиль если нужно
        if self.current_profile_name == old_name:
            self.current_profile_name = new_name

        return True

    def get_profile_names(self) -> list:
        """Получает список имен профилей."""
        return sorted(self.profiles.keys())

    def get_profiles_count(self) -> int:
        """Получает количество профилей."""
        return len(self.profiles)

    def export_profile(self, profile_name: str, file_path: str) -> bool:
        """
        Экспортирует профиль в файл.

        Args:
            profile_name: Имя профиля для экспорта
            file_path: Путь для сохранения

        Returns:
            True если экспорт успешен
        """
        if profile_name not in self.profiles:
            return False

        try:
            profile_data = {
                'profile_name': profile_name,
                'profile_data': self.profiles[profile_name].to_dict(),
                'exported_at': datetime.now().isoformat(),
                'version': '1.0'
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)

            return True

        except Exception:
            return False

    def import_profile(self, file_path: str) -> bool:
        """
        Импортирует профиль из файла.

        Args:
            file_path: Путь к файлу профиля

        Returns:
            True если импорт успешен
        """
        if not os.path.exists(file_path):
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)

            # Поддержка разных форматов
            if 'profile_name' in import_data and 'profile_data' in import_data:
                profile_name = import_data['profile_name']
                profile_data = import_data['profile_data']
            elif 'mappings' in import_data:
                # Старый формат
                profile_name = os.path.splitext(os.path.basename(file_path))[0]
                profile_data = import_data
            else:
                return False

            # Создаем или перезаписываем профиль
            self.profiles[profile_name] = Profile.from_dict(profile_name, profile_data)
            return True

        except Exception:
            return False