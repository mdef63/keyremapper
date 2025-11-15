"""
Мониторинг активных процессов Windows.
"""
import threading
import time
from typing import Optional
from constants import WINDOWS_API_AVAILABLE, PROCESS_MONITOR_INTERVAL


class ProcessMonitor:
    """Мониторинг активных процессов Windows."""

    def __init__(self, target_process: str):
        self.target_process = target_process
        self.current_process: Optional[str] = None
        self.is_target_active = False
        self.monitor_running = False
        self.monitor_thread: Optional[threading.Thread] = None
        self._process_cache = None
        self._last_process_check = 0
        self._process_check_interval = 0.1

    def start_monitoring(self):
        """Запускает фоновый мониторинг процессов."""
        if self.monitor_running:
            return

        self.monitor_running = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_worker,
            daemon=True,
            name="ProcessMonitor"
        )
        self.monitor_thread.start()

    def stop_monitoring(self):
        """Останавливает мониторинг процессов."""
        self.monitor_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
            self.monitor_thread = None

    def _monitor_worker(self):
        """Фоновый поток для мониторинга изменений процесса."""
        while self.monitor_running:
            try:
                current_process = self._get_active_window_process()

                # Обновляем информацию о процессе
                self.current_process = current_process
                self.is_target_active = self._is_target_process_active(use_cache=False)

                time.sleep(PROCESS_MONITOR_INTERVAL)

            except Exception as e:
                print(f"Process monitor error: {e}")
                time.sleep(1.0)

    def _get_active_window_process(self) -> Optional[str]:
        """
        Получает имя процесса активного окна.

        Returns:
            Имя процесса или None при ошибке
        """
        if not WINDOWS_API_AVAILABLE:
            return None

        try:
            import win32gui
            import win32process
            import psutil

            # Получаем handle активного окна
            hwnd = win32gui.GetForegroundWindow()
            if hwnd == 0:
                return None

            # Получаем ID процесса
            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            # Получаем имя процесса
            process = psutil.Process(pid)
            return process.name()

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None
        except Exception:
            return None

    def _is_target_process_active(self, use_cache: bool = True) -> bool:
        """
        Проверяет, является ли активное окно целевым процессом.

        Args:
            use_cache: Использовать кэшированный результат

        Returns:
            True если активный процесс соответствует целевому
        """
        if not WINDOWS_API_AVAILABLE:
            return True  # Fallback если Windows API недоступно

        # Используем кэш для оптимизации
        current_time = time.time()
        if (use_cache and self._process_cache is not None and
            (current_time - self._last_process_check) < self._process_check_interval):
            return self._process_cache

        active_process = self._get_active_window_process()
        if active_process is None:
            self._process_cache = False
            self._last_process_check = current_time
            return False

        # Гибкое сравнение процессов
        active_lower = active_process.lower()
        target_lower = self.target_process.lower()

        result = (
            active_lower == target_lower or
            active_lower.startswith(target_lower) or
            active_lower.endswith(target_lower) or
            target_lower in active_lower or
            active_lower in target_lower
        )

        # Обновляем кэш
        self._process_cache = result
        self._last_process_check = current_time

        return result

    def get_current_process_display(self) -> str:
        """
        Получает отформатированную информацию о текущем процессе для отображения.

        Returns:
            Строка с информацией о процессе
        """
        if not WINDOWS_API_AVAILABLE:
            return "Определение процесса недоступно"

        status_icon = "✅" if self.is_target_active else "❌"
        process_name = self.current_process or "Не определен"
        return f"{status_icon} {process_name}"

    def get_detailed_status(self) -> dict:
        """
        Получает детальную информацию о статусе процесса.

        Returns:
            Словарь с детальной информацией
        """
        return {
            'current_process': self.current_process,
            'target_process': self.target_process,
            'is_target_active': self.is_target_active,
            'monitor_running': self.monitor_running
        }

    def update_target_process(self, new_target: str):
        """
        Обновляет целевой процесс.

        Args:
            new_target: Новый целевой процесс
        """
        self.target_process = new_target
        # Сбрасываем кэш при изменении целевого процесса
        self._process_cache = None

    def get_running_processes(self, filter_term: str = "") -> list:
        """
        Получает список запущенных процессов.

        Args:
            filter_term: Фильтр для поиска процессов

        Returns:
            Список имен процессов
        """
        if not WINDOWS_API_AVAILABLE:
            return []

        try:
            import psutil

            processes = []
            seen_names = set()

            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name']
                    if proc_name and proc_name not in seen_names:
                        seen_names.add(proc_name)
                        if not filter_term or filter_term.lower() in proc_name.lower():
                            processes.append(proc_name)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            return sorted(processes)

        except Exception as e:
            print(f"⚠️  Ошибка при получении списка процессов: {e}")
            return []