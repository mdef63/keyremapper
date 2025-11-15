"""
Мониторинг процессов для приложения переназначения клавиш.
"""

import time
import threading
from typing import Optional

from constants import WINDOWS_API_AVAILABLE, PROCESS_MONITOR_INTERVAL


class ProcessMonitor:
    """Мониторинг активного процесса."""

    def __init__(self):
        self._process_cache = None
        self._last_process_check = 0
        self.current_process_info = "Не определен"
        self.process_match_status = "❌"
        self.last_active_process = None
        self.monitor_running = False
        self.process_monitor_thread = None

    def get_active_window_process(self) -> Optional[str]:
        """Получить имя процесса активного окна."""
        if not WINDOWS_API_AVAILABLE:
            return None

        try:
            import win32gui
            import win32process
            import psutil

            hwnd = win32gui.GetForegroundWindow()
            if hwnd == 0:
                return None

            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied, Exception):
            return None

    def is_target_process_active(self, target_process: str, use_cache: bool = True) -> bool:
        """Проверка, является ли активное окно целевым процессом."""
        if not WINDOWS_API_AVAILABLE:
            return True

        current_time = time.time()
        if use_cache and self._process_cache is not None and \
                (current_time - self._last_process_check) < 0.1:  # PROCESS_CHECK_INTERVAL
            return self._process_cache

        active_process = self.get_active_window_process()
        if active_process is None:
            self._process_cache = False
            self._last_process_check = current_time
            return False

        active_lower = active_process.lower()
        target_lower = target_process.lower()

        result = (
            active_lower == target_lower or
            active_lower.startswith(target_lower) or
            active_lower.endswith(target_lower) or
            target_lower in active_lower or
            active_lower in target_lower
        )

        self._process_cache = result
        self._last_process_check = current_time
        return result

    def start_monitoring(self) -> None:
        """Запуск фонового мониторинга процессов."""
        if self.monitor_running:
            return

        self.monitor_running = True
        self.process_monitor_thread = threading.Thread(
            target=self._monitor_worker,
            daemon=True
        )
        self.process_monitor_thread.start()

    def stop_monitoring(self) -> None:
        """Остановка мониторинга процессов."""
        self.monitor_running = False
        if self.process_monitor_thread:
            self.process_monitor_thread.join(timeout=1.0)
            self.process_monitor_thread = None

    def _monitor_worker(self) -> None:
        """Фоновый поток для мониторинга изменений процесса."""
        while self.monitor_running:
            try:
                current_process = self.get_active_window_process()

                if current_process:
                    self.current_process_info = current_process
                    # Note: target_process is passed from outside when checking
                    # We update the display but the actual check is done in the remapper
                    self.process_match_status = "❌"  # Default, will be updated by remapper
                else:
                    self.current_process_info = "Не определен"
                    self.process_match_status = "❌"

                if current_process != self.last_active_process:
                    self.last_active_process = current_process
                    self._process_cache = None  # Reset cache on process change

                time.sleep(PROCESS_MONITOR_INTERVAL)
            except Exception as e:
                print(f"Process monitor error: {e}")
                time.sleep(1.0)