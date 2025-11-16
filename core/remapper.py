"""
Основной класс ремаппера для приложения переназначения клавиш.
"""

import time
import keyboard
from typing import Dict, List, Optional

from core.config_manager import ConfigManager
from core.process_monitor import ProcessMonitor
from core.action_executor import ActionExecutor
from core.settings_manager import SettingsManager, AutoStartManager
from utils.macro_manager import MacroManager


class KeyboardRemapper:
    """Основной класс для переназначения клавиш."""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.process_monitor = ProcessMonitor()
        self.action_executor = ActionExecutor()

        self.mappings: Dict[str, str] = {}
        self.is_active = False
        self.hotkeys = []

        self.load_config()

        self.settings_manager = SettingsManager()
        self.macro_manager = MacroManager(self.config_manager)
        self.autostart_manager = AutoStartManager()

    def load_config(self) -> None:
        """Загрузка конфигурации из файла."""
        try:
            if self.config_manager.load_config():
                current_profile = self.config_manager.get_current_profile()
                self.mappings = current_profile.mappings.copy()  # Используем копию
            else:
                # Инициализация по умолчанию
                self.mappings = {}
                print("📝 Используется конфигурация по умолчанию")
        except Exception as e:
            print(f"❌ Ошибка при загрузке конфигурации: {e}")
            self.mappings = {}

    def save_config(self, create_backup: bool = True, show_message: bool = True) -> bool:
        """Сохранение конфигурации в файл."""
        try:
            current_profile = self.config_manager.get_current_profile()
            current_profile.mappings = self.mappings.copy()  # Сохраняем копию
            success = self.config_manager.save_config(create_backup=create_backup)
            if success and show_message:
                print("✅ Конфигурация сохранена")
            return success
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return False

    def start_remapping(self) -> None:
        """Запуск переназначения."""
        if not self.mappings:
            print("❌ Нет назначенных клавиш!")
            return

        print("\n🚀 Запуск переназначения...")
        print("📋 Активные назначения:")

        # Ленивый импорт для избежания циклических зависимостей
        from utils.formatters import format_key_display, get_action_display

        for key, action in self.mappings.items():
            display_action = get_action_display(action)
            display_key = format_key_display(key)
            print(f"  {display_key} → {display_action}")

        # Проверяем доступность Windows API
        if not self.process_monitor.get_active_window_process():
            print("⚠️  Не удалось определить активный процесс. Переназначение будет работать для всех окон.")

        # Запускаем мониторинг процессов
        self.process_monitor.start_monitoring()

        current_profile = self.config_manager.get_current_profile()
        print(f"\n🎯 Переназначение работает ТОЛЬКО для процесса: {current_profile.target_process}")
        print("💡 Переключитесь на окно с целевым процессом и нажимайте клавиши")
        print("⏹️  Для остановки нажмите Ctrl+C в этом окне")

        # Регистрируем горячие клавиши
        hotkeys = []
        registered_count = 0

        for key, action in self.mappings.items():
            def make_handler(a, k):
                def handler():
                    # Проверяем, активен ли целевой процесс
                    current_profile = self.config_manager.get_current_profile()
                    if not self.process_monitor.is_target_process_active(current_profile.target_process, use_cache=True):
                        # Если процесс не активен, отправляем оригинальную клавишу
                        try:
                            keyboard.send(k)
                        except:
                            pass
                        return

                    # Выполняем действие
                    try:
                        self.action_executor.execute_action(a)
                    except Exception as e:
                        print(f"\n⚠️  Ошибка при выполнении действия для {k}: {e}")

                return handler

            handler = make_handler(action, key)
            try:
                hotkey = keyboard.add_hotkey(key, handler, suppress=True)
                hotkeys.append(hotkey)
                registered_count += 1

                from utils.formatters import format_key_display
                print(f"✅ Зарегистрировано: {format_key_display(key)}")
            except Exception as e:
                from utils.formatters import format_key_display
                print(f"⚠️  Не удалось зарегистрировать {format_key_display(key)}: {e}")

        if registered_count == 0:
            print("\n❌ Не удалось зарегистрировать ни одной клавиши!")
            self.process_monitor.stop_monitoring()
            return

        print("\n🎯 Переназначение активно!")

        try:
            keyboard.wait()
        except KeyboardInterrupt:
            print("\n🛑 Остановка...")
        finally:
            self.process_monitor.stop_monitoring()
            for hotkey in hotkeys:
                try:
                    keyboard.remove_hotkey(hotkey)
                except:
                    pass
            print("✅ Переназначение остановлено")

    def show_mappings(self) -> None:
        """Показать текущие назначения."""
        if not self.mappings:
            print("📝 Нет назначенных клавиш")
            return

        print("\n📋 Текущие назначения:")

        from utils.formatters import format_key_display, get_action_display

        for key, action in self.mappings.items():
            display_action = get_action_display(action)
            display_key = format_key_display(key)
            print(f"  {display_key} → {display_action}")

    # Новые методы для расширенной функциональности
    def get_quick_profiles(self):
        """Возвращает доступные быстрые профили."""
        try:
            from constants import QUICK_PROFILES
            return QUICK_PROFILES
        except ImportError:
            return {}

    def create_quick_profile(self, profile_id: str, custom_name: str = None) -> bool:
        """Создает профиль на основе быстрого шаблона."""
        quick_profiles = self.get_quick_profiles()

        if profile_id not in quick_profiles:
            return False

        profile_info = quick_profiles[profile_id]
        profile_name = custom_name or profile_info['name']

        # Создаем новый профиль
        from models.profile import Profile
        new_profile = Profile(
            name=profile_name,
            mappings=profile_info.get('preset_mappings', {}),
            target_process=profile_info.get('target_process', 'Yandex')
        )

        # Добавляем в конфигурацию
        self.config_manager.profiles[profile_name] = new_profile
        self.config_manager.current_profile_name = profile_name
        self.mappings = new_profile.mappings.copy()

        return self.save_config()

    def create_backup_with_description(self, description: str = "") -> bool:
        """Создает резервную копию с описанием."""
        try:
            from utils.backup_manager import BackupManager
            backup_manager = BackupManager()
            backup_path = backup_manager.create_backup(description)
            return backup_path is not None
        except Exception as e:
            print(f"❌ Ошибка создания резервной копии: {e}")
            return False

    def get_macro_manager(self):
        """Возвращает менеджер макросов."""
        return self.macro_manager

    def get_settings_manager(self):
        """Возвращает менеджер настроек."""
        return self.settings_manager

    def execute_macro(self, macro_name: str) -> bool:
        """Выполняет макрос."""
        return self.macro_manager.execute_macro(macro_name, self.action_executor)

    def create_macro_from_mapping(self, key: str, macro_name: str = None) -> bool:
        """Создает макрос из существующего назначения."""
        if key not in self.mappings:
            return False

        if not macro_name:
            macro_name = f"macro_{key}"

        action = self.mappings[key]
        return self.macro_manager.create_macro(
            name=macro_name,
            action_type="action",
            value=action,
            description=f"Макрос из назначения {key}",
            category="imported"
        )

    def import_all_mappings_to_macros(self) -> int:
        """Импортирует все назначения в макросы."""
        return self.macro_manager.import_macros_from_mappings(self.mappings)