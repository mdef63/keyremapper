"""
Основной класс для переназначения клавиш.
"""
import keyboard
from typing import List, Optional
from models.profile import Profile
from models.mapping import MappingManager
from core.config_manager import ConfigManager
from core.process_monitor import ProcessMonitor
from core.action_executor import ActionExecutor
from utils.validators import KeyValidator
from utils.formatters import DisplayFormatter


class KeyboardRemapper:
    """Основной класс для управления переназначением клавиш."""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.process_monitor: Optional[ProcessMonitor] = None
        self.action_executor = ActionExecutor()
        self.mapping_manager = MappingManager()
        self.hotkeys: List[keyboard.HotKey] = []
        self.is_active = False

        # Загружаем конфигурацию
        self._load_configuration()

    def _load_configuration(self):
        """Загружает конфигурацию и инициализирует компоненты."""
        self.config_manager.load_config()

        # Получаем текущий профиль
        current_profile = self.config_manager.get_current_profile()
        if current_profile:
            self.mapping_manager.from_dict(current_profile.mappings)
            target_process = current_profile.target_process
        else:
            target_process = "Yandex"

        # Инициализируем мониторинг процессов
        self.process_monitor = ProcessMonitor(target_process)
        self.process_monitor.start_monitoring()

    def get_current_profile(self) -> Optional[Profile]:
        """Получает текущий профиль."""
        return self.config_manager.get_current_profile()

    def get_current_process_display(self) -> str:
        """Получает отформатированную информацию о текущем процессе."""
        if self.process_monitor:
            return self.process_monitor.get_current_process_display()
        return "Мониторинг не инициализирован"

    def get_target_process(self) -> str:
        """Получает целевой процесс."""
        if self.process_monitor:
            return self.process_monitor.target_process
        return "Yandex"

    def set_target_process(self, target_process: str):
        """Устанавливает целевой процесс."""
        if self.process_monitor:
            self.process_monitor.update_target_process(target_process)

        # Обновляем в текущем профиле
        current_profile = self.get_current_profile()
        if current_profile:
            current_profile.target_process = target_process

    def add_mapping(self, key: str, action: str) -> bool:
        """
        Добавляет новое назначение клавиши.

        Args:
            key: Клавиша или комбинация
            action: Действие

        Returns:
            True если назначение добавлено
        """
        # Валидируем клавишу
        validated_key = KeyValidator.validate_key(key)
        if not validated_key:
            return False

        # Добавляем назначение
        self.mapping_manager.add(validated_key, action)

        # Сохраняем конфигурацию
        self._save_current_profile()
        return True

    def remove_mapping(self, key: str) -> bool:
        """
        Удаляет назначение клавиши.

        Args:
            key: Клавиша для удаления

        Returns:
            True если назначение удалено
        """
        success = self.mapping_manager.remove(key)
        if success:
            self._save_current_profile()
        return success

    def edit_mapping(self, key: str, new_action: str) -> bool:
        """
        Редактирует существующее назначение.

        Args:
            key: Клавиша для редактирования
            new_action: Новое действие

        Returns:
            True если назначение обновлено
        """
        if not self.mapping_manager.exists(key):
            return False

        self.mapping_manager.add(key, new_action)
        self._save_current_profile()
        return True

    def get_mappings(self) -> List[tuple]:
        """Получает все назначения."""
        return self.mapping_manager.get_all()

    def search_mappings(self, search_term: str) -> List[tuple]:
        """
        Ищет назначения по поисковому запросу.

        Args:
            search_term: Поисковый запрос

        Returns:
            Список найденных назначений
        """
        return self.mapping_manager.search(search_term)

    def test_mapping(self, key: str) -> bool:
        """
        Тестирует назначение без запуска remapping.

        Args:
            key: Клавиша для тестирования

        Returns:
            True если тестирование успешно
        """
        action = self.mapping_manager.get(key)
        if not action:
            return False

        try:
            self.action_executor.execute_action(action)
            return True
        except Exception:
            return False

    def start_remapping(self) -> bool:
        """
        Запускает переназначение клавиш.

        Returns:
            True если переназначение успешно запущено
        """
        if self.is_active:
            return True

        if self.mapping_manager.count() == 0:
            print("❌ Нет назначенных клавиш!")
            return False

        # Регистрируем горячие клавиши
        registered_count = 0
        for key, action in self.mapping_manager.get_all():
            try:
                hotkey = self._create_hotkey_handler(key, action)
                self.hotkeys.append(hotkey)
                registered_count += 1
            except Exception as e:
                print(f"⚠️  Не удалось зарегистрировать {key}: {e}")

        if registered_count == 0:
            print("❌ Не удалось зарегистрировать ни одной клавиши!")
            return False

        self.is_active = True
        print(f"🎯 Переназначение активно ({registered_count} клавиш)")
        return True

    def stop_remapping(self):
        """Останавливает переназначение клавиш."""
        if not self.is_active:
            return

        # Удаляем все горячие клавиши
        for hotkey in self.hotkeys:
            try:
                keyboard.remove_hotkey(hotkey)
            except Exception:
                pass

        self.hotkeys.clear()
        self.is_active = False
        print("✅ Переназначение остановлено")

    def _create_hotkey_handler(self, key: str, action: str):
        """
        Создает обработчик для горячей клавиши.

        Args:
            key: Клавиша
            action: Действие

        Returns:
            Объект горячей клавиши
        """
        def handler():
            # Проверяем, активен ли целевой процесс
            if (self.process_monitor and
                not self.process_monitor._is_target_process_active(use_cache=True)):
                # Если процесс не активен, отправляем оригинальную клавишу
                try:
                    keyboard.send(key)
                except Exception:
                    pass
                return

            # Выполняем действие
            self.action_executor.execute_action(action)

        return keyboard.add_hotkey(key, handler, suppress=True)

    def _save_current_profile(self):
        """Сохраняет текущий профиль в конфигурацию."""
        current_profile = self.get_current_profile()
        if current_profile:
            current_profile.mappings = self.mapping_manager.to_dict()
            self.config_manager.save_config(create_backup=False)

    def save_configuration(self) -> bool:
        """Сохраняет всю конфигурацию."""
        self._save_current_profile()
        return self.config_manager.save_config()

    def switch_profile(self, profile_name: str) -> bool:
        """
        Переключается на другой профиль.

        Args:
            profile_name: Имя профиля

        Returns:
            True если переключение успешно
        """
        if self.is_active:
            self.stop_remapping()

        success = self.config_manager.set_current_profile(profile_name)
        if success:
            # Обновляем mappings из нового профиля
            current_profile = self.get_current_profile()
            if current_profile:
                self.mapping_manager.from_dict(current_profile.mappings)
                # Обновляем целевой процесс в мониторинге
                if self.process_monitor:
                    self.process_monitor.update_target_process(current_profile.target_process)

        return success

    def cleanup(self):
        """Очищает ресурсы."""
        self.stop_remapping()
        if self.process_monitor:
            self.process_monitor.stop_monitoring()