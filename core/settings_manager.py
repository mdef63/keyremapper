"""
Менеджер настроек приложения.
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

from models.settings import AppSettings


class SettingsManager:
    """Управление настройками приложения."""

    def __init__(self):
        self.settings_file = Path("app_settings.json")
        self.settings = AppSettings()
        self.load_settings()

    def load_settings(self) -> bool:
        """Загружает настройки из файла."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings_data = json.load(f)

                self.settings = AppSettings.from_dict(settings_data)
                return True
            else:
                # Создаем настройки по умолчанию
                self.save_settings()
                return True
        except Exception as e:
            print(f"❌ Ошибка загрузки настроек: {e}")
            return False

    def save_settings(self) -> bool:
        """Сохраняет настройки в файл."""
        try:
            settings_data = self.settings.to_dict()

            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения настроек: {e}")
            return False

    def get_setting(self, key: str) -> Any:
        """Возвращает значение настройки."""
        return getattr(self.settings, key, None)

    def set_setting(self, key: str, value: Any) -> bool:
        """Устанавливает значение настройки."""
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)
            return self.save_settings()
        return False

    def reset_settings(self) -> bool:
        """Сбрасывает настройки к значениям по умолчанию."""
        self.settings = AppSettings()
        return self.save_settings()

    def get_all_settings(self) -> Dict[str, Any]:
        """Возвращает все настройки."""
        return self.settings.to_dict()


class AutoStartManager:
    """Управление автозагрузкой приложения."""

    def __init__(self, app_name: str = "KeyboardRemapper"):
        self.app_name = app_name
        self.setup_autostart_methods()

    def setup_autostart_methods(self) -> None:
        """Настраивает методы автозагрузки в зависимости от ОС."""
        if os.name == 'nt':  # Windows
            self.enable_autostart = self._enable_autostart_windows
            self.disable_autostart = self._disable_autostart_windows
            self.is_autostart_enabled = self._is_autostart_enabled_windows
        else:  # Linux/Mac
            self.enable_autostart = self._enable_autostart_linux
            self.disable_autostart = self._disable_autostart_linux
            self.is_autostart_enabled = self._is_autostart_enabled_linux

    def _enable_autostart_windows(self) -> bool:
        """Включает автозагрузку в Windows."""
        try:
            import winreg

            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"

            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as registry_key:
                winreg.SetValueEx(registry_key, self.app_name, 0, winreg.REG_SZ,
                                  f'"{os.path.abspath(sys.argv[0])}"')

            return True
        except Exception as e:
            print(f"❌ Ошибка включения автозагрузки: {e}")
            return False

    def _disable_autostart_windows(self) -> bool:
        """Выключает автозагрузку в Windows."""
        try:
            import winreg

            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"

            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as registry_key:
                winreg.DeleteValue(registry_key, self.app_name)

            return True
        except Exception:
            # Если ключа нет, считаем что автозагрузка отключена
            return True

    def _is_autostart_enabled_windows(self) -> bool:
        """Проверяет включена ли автозагрузка в Windows."""
        try:
            import winreg

            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"

            with winreg.OpenKey(key, subkey, 0, winreg.KEY_READ) as registry_key:
                try:
                    winreg.QueryValueEx(registry_key, self.app_name)
                    return True
                except FileNotFoundError:
                    return False
        except Exception:
            return False

    def _enable_autostart_linux(self) -> bool:
        """Включает автозагрузку в Linux."""
        try:
            autostart_dir = Path.home() / '.config' / 'autostart'
            autostart_dir.mkdir(parents=True, exist_ok=True)

            desktop_file = autostart_dir / f'{self.app_name}.desktop'

            desktop_content = f"""[Desktop Entry]
Type=Application
Name={self.app_name}
Exec={os.path.abspath(sys.argv[0])}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
"""

            with open(desktop_file, 'w') as f:
                f.write(desktop_content)

            return True
        except Exception as e:
            print(f"❌ Ошибка включения автозагрузки: {e}")
            return False

    def _disable_autostart_linux(self) -> bool:
        """Выключает автозагрузку в Linux."""
        try:
            desktop_file = Path.home() / '.config' / 'autostart' / f'{self.app_name}.desktop'
            if desktop_file.exists():
                desktop_file.unlink()
            return True
        except Exception:
            return False

    def _is_autostart_enabled_linux(self) -> bool:
        """Проверяет включена ли автозагрузка в Linux."""
        desktop_file = Path.home() / '.config' / 'autostart' / f'{self.app_name}.desktop'
        return desktop_file.exists()