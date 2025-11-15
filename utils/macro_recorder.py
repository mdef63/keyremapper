"""
Запись макросов для приложения переназначения клавиш.
"""

import time
import threading
from typing import List, Dict, Any, Optional, Callable


class MacroRecorder:
    """Запись и воспроизведение макросов."""

    def __init__(self):
        self.is_recording = False
        self.recorded_events: List[Dict[str, Any]] = []
        self.start_time: Optional[float] = None
        self.on_record_callback: Optional[Callable] = None

    def start_recording(self) -> bool:
        """Начинает запись макроса."""
        if self.is_recording:
            return False

        self.is_recording = True
        self.recorded_events = []
        self.start_time = time.time()

        print("🔴 Запись макроса начата...")
        print("💡 Нажимайте клавиши для записи")
        print("⏹️  Для остановки нажмите F12")

        return True

    def stop_recording(self) -> List[Dict[str, Any]]:
        """Останавливает запись макроса."""
        if not self.is_recording:
            return []

        self.is_recording = False
        recording_duration = time.time() - self.start_time

        print(f"⏹️  Запись остановлена. Длительность: {recording_duration:.1f}с")
        print(f"📝 Записано событий: {len(self.recorded_events)}")

        return self.recorded_events

    def record_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Записывает событие."""
        if not self.is_recording:
            return

        event = {
            'type': event_type,
            'data': data,
            'timestamp': time.time() - self.start_time,
            'time_since_last': self._get_time_since_last()
        }

        self.recorded_events.append(event)

    def play_macro(self, events: List[Dict[str, Any]], speed: float = 1.0) -> None:
        """Воспроизводит записанный макрос."""
        import keyboard

        print("▶️  Воспроизведение макроса...")

        for i, event in enumerate(events):
            if i > 0 and 'time_since_last' in event:
                delay = event['time_since_last'] / speed
                time.sleep(delay)

            if event['type'] == 'key_press':
                keyboard.press(event['data']['key'])
            elif event['type'] == 'key_release':
                keyboard.release(event['data']['key'])

        print("✅ Воспроизведение завершено")

    def convert_to_mapping(self, events: List[Dict[str, Any]], name: str):
        """Конвертирует записанные события в макрос."""
        if not events:
            return None

        # Пока просто создаем текстовый макрос из нажатых клавиш
        key_sequence = []
        for event in events:
            if event['type'] in ['key_press', 'key_release']:
                key = event['data']['key']
                if key not in key_sequence:
                    key_sequence.append(key)

        if key_sequence:
            key_combo = '+'.join(key_sequence)

            # Создаем экземпляр Macro
            from models.mapping import Macro
            return Macro(
                name=name,
                action_type="key_combo",
                value=key_combo,
                description=f"Записанный макрос: {key_combo}"
            )

        return None

    def _get_time_since_last(self) -> float:
        """Возвращает время с последнего события."""
        if not self.recorded_events:
            return 0.0
        return time.time() - self.start_time - self.recorded_events[-1]['timestamp']