"""
Функции для отображения информации в реальном времени.
"""
import time
from core.process_monitor import ProcessMonitor


class RealTimeDisplay:
    """Отображение информации в реальном времени."""

    @staticmethod
    def show_process_status(process_monitor: ProcessMonitor):
        """
        Показывает текущий статус процесса в реальном времени.

        Args:
            process_monitor: Монитор процессов для получения данных
        """
        print("\n🖥️  Текущий статус процесса:")
        print("Нажмите Ctrl+C для возврата в меню")

        try:
            while True:
                current_process = process_monitor.get_active_window_process()
                is_target = process_monitor.is_target_process_active(use_cache=False)

                status_icon = "✅" if is_target else "❌"
                print(
                    f"\r{status_icon} Активный процесс: {current_process or 'Не определен'} | "
                    f"Целевой: {process_monitor.target_process} | "
                    f"Работает: {'ДА' if is_target else 'НЕТ'}",
                    end="",
                    flush=True
                )

                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n\n🔙 Возврат в меню...")