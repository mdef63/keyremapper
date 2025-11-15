"""
Менеджер резервных копий для приложения переназначения клавиш.
"""

import os
import shutil
import zipfile
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from constants import BACKUP_DIR, CONFIG_FILE


class BackupManager:
    """Управление резервными копиями конфигурации."""

    def __init__(self, max_backups: int = 10):
        self.max_backups = max_backups
        self.backup_dir = Path(BACKUP_DIR)
        self.backup_dir.mkdir(exist_ok=True)

    def create_backup(self, description: str = "") -> Optional[str]:
        """Создает резервную копию конфигурации."""
        if not os.path.exists(CONFIG_FILE):
            return None

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desc_suffix = f"_{description}" if description else ""
            backup_file = self.backup_dir / f"config_backup_{timestamp}{desc_suffix}.json"

            shutil.copy2(CONFIG_FILE, backup_file)

            # Очистка старых резервных копий
            self._cleanup_old_backups()

            return str(backup_file)
        except Exception as e:
            print(f"⚠️  Не удалось создать резервную копию: {e}")
            return None

    def create_zip_backup(self, include_logs: bool = False) -> Optional[str]:
        """Создает zip-архив с резервной копией."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_path = self.backup_dir / f"full_backup_{timestamp}.zip"

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Добавляем конфигурацию
                if os.path.exists(CONFIG_FILE):
                    zipf.write(CONFIG_FILE, "key_config.json")

                # Добавляем логи если нужно
                if include_logs and os.path.exists("logs"):
                    for log_file in Path("logs").glob("*.log"):
                        zipf.write(log_file, f"logs/{log_file.name}")

            self._cleanup_old_backups()
            return str(zip_path)
        except Exception as e:
            print(f"❌ Ошибка создания zip-архива: {e}")
            return None

    def list_backups(self) -> List[dict]:
        """Возвращает список резервных копий."""
        backups = []
        for backup_file in self.backup_dir.glob("*.json"):
            stat = backup_file.stat()
            backups.append({
                'path': str(backup_file),
                'name': backup_file.name,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'description': self._extract_description(backup_file.name)
            })

        return sorted(backups, key=lambda x: x['created'], reverse=True)

    def restore_backup(self, backup_path: str) -> bool:
        """Восстанавливает конфигурацию из резервной копии."""
        try:
            if not os.path.exists(backup_path):
                return False

            # Создаем резервную копию текущей конфигурации
            current_backup = self.create_backup("before_restore")

            shutil.copy2(backup_path, CONFIG_FILE)
            print(f"✅ Конфигурация восстановлена из {os.path.basename(backup_path)}")
            if current_backup:
                print(f"💾 Текущая конфигурация сохранена в {os.path.basename(current_backup)}")

            return True
        except Exception as e:
            print(f"❌ Ошибка восстановления: {e}")
            return False

    def delete_backup(self, backup_path: str) -> bool:
        """Удаляет резервную копию."""
        try:
            os.remove(backup_path)
            return True
        except Exception as e:
            print(f"❌ Ошибка удаления резервной копии: {e}")
            return False

    def _cleanup_old_backups(self) -> None:
        """Удаляет старые резервные копии."""
        backups = self.list_backups()
        if len(backups) > self.max_backups:
            for backup in backups[self.max_backups:]:
                try:
                    os.remove(backup['path'])
                except Exception:
                    pass

    def _extract_description(self, filename: str) -> str:
        """Извлекает описание из имени файла."""
        if '_' in filename:
            parts = filename.split('_')
            if len(parts) > 3:
                return parts[3].replace('.json', '')
        return ""