"""
Меню и навигация для приложения переназначения клавиш.
"""

import time
from typing import Optional

from utils.helpers import clear_screen
from ui.dialogs import (
    add_mapping_dialog, edit_mapping_dialog, remove_mapping_dialog,
    test_mapping_dialog, search_mappings_dialog,
    list_profiles_dialog, create_profile_dialog, switch_profile_dialog,
    duplicate_profile_dialog, rename_profile_dialog, delete_profile_dialog,
    change_target_process_dialog, detect_current_process_dialog,
    export_profile_dialog, import_profile_dialog, show_statistics_dialog,
    show_info_dialog
)
from ui.advanced_dialogs import (
    backup_management_dialog, macro_recording_dialog, quick_profile_dialog,
    settings_dialog
)


def main_menu(remapper) -> None:
    """Главное меню программы."""
    remapper.process_monitor.start_monitoring()

    while True:
        clear_screen()
        print("\n" + "=" * 60)
        print("🎹 ПЕРЕНАЗНАЧЕНИЕ КЛАВИШ - РЕАЛЬНОЕ ВРЕМЯ")
        print("=" * 60)
        current_profile = remapper.config_manager.get_current_profile()
        print(f"📌 Текущий профиль: {current_profile.name}")
        print(f"🎯 Целевой процесс: {current_profile.target_process}")
        print(f"🖥️  Активный процесс: {remapper.process_monitor.current_process_info} {remapper.process_monitor.process_match_status}")
        print("=" * 60)
        print("1. 📋 Показать текущие назначения")
        print("2. ➕ Добавить назначение")
        print("3. ✏️  Редактировать назначение")
        print("4. ❌ Удалить назначение")
        print("5. 🔍 Поиск назначений")
        print("6. 🧪 Тестировать назначение")
        print("7. 🚀 Запустить переназначение")
        print("8. 👤 Управление профилями")
        print("9. 📊 Статистика")

        # Новые пункты меню
        print("C. 💾 Управление резервными копиями")
        print("D. 🎙️  Запись макросов")
        print("E. 🚀 Быстрые профили")
        print("F. ⚙️  Настройки приложения")

        print("A. ℹ️  Информация о программе")
        print("B. 🖥️  Показать текущий статус процесса (детальный)")
        print("0. 🚪 Выйти")

        choice = input("\n🎯 Выберите действие (0-9, A-F): ").strip().upper()

        if choice == '1':
            remapper.show_mappings()
            input("\nНажмите Enter для продолжения...")
        elif choice == '2':
            add_mapping_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '3':
            edit_mapping_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '4':
            remove_mapping_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '5':
            search_mappings_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '6':
            test_mapping_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '7':
            remapper.start_remapping()
            input("\nНажмите Enter для продолжения...")
        elif choice == '8':
            manage_profiles_menu(remapper)
        elif choice == '9':
            show_statistics_dialog(remapper)
            input("\nНажмите Enter для продолжения...")

        # Новые обработчики
        elif choice == 'C':
            backup_management_dialog(remapper)
        elif choice == 'D':
            macro_recording_dialog(remapper)
        elif choice == 'E':
            quick_profile_dialog(remapper)
        elif choice == 'F':
            settings_dialog(remapper)

        elif choice == 'A' or choice == 'А':
            show_info_dialog()
            input("\nНажмите Enter для продолжения...")
        elif choice == 'B':
            show_current_process_status(remapper)
        elif choice == '0':
            print("👋 До свидания!")
            remapper.process_monitor.stop_monitoring()
            break
        else:
            print("❌ Неверный выбор, попробуйте снова")
            time.sleep(1)


def manage_profiles_menu(remapper) -> None:
    """Меню управления профилями."""
    while True:
        clear_screen()
        print("\n" + "=" * 50)
        print("👤 УПРАВЛЕНИЕ ПРОФИЛЯМИ")
        print("=" * 50)
        current_profile = remapper.config_manager.get_current_profile()
        print(f"📌 Текущий профиль: {current_profile.name}")
        print(f"🎯 Целевой процесс: {current_profile.target_process}")
        print(f"🖥️  Активный процесс: {remapper.process_monitor.current_process_info} {remapper.process_monitor.process_match_status}")
        print("=" * 50)
        print("1. 📋 Список профилей")
        print("2. ➕ Создать профиль")
        print("3. 🔄 Переключить профиль")
        print("4. 📋 Дублировать профиль")
        print("5. ✏️  Переименовать профиль")
        print("6. ❌ Удалить профиль")
        print("7. ⚙️  Изменить целевой процесс текущего профиля")
        print("8. 🔍 Определить текущий активный процесс")
        print("9. 💾 Экспортировать профиль")
        print("A. 📥 Импортировать профиль")
        print("0. 🔙 Назад")

        choice = input("\n🎯 Выберите действие (0-9, A): ").strip().upper()

        if choice == '1':
            list_profiles_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '2':
            create_profile_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '3':
            switch_profile_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '4':
            duplicate_profile_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '5':
            rename_profile_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '6':
            delete_profile_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '7':
            change_target_process_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '8':
            detect_current_process_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '9':
            export_profile_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == 'A' or choice == 'А':
            import_profile_dialog(remapper)
            input("\nНажмите Enter для продолжения...")
        elif choice == '0':
            break
        else:
            print("❌ Неверный выбор, попробуйте снова")
            time.sleep(1)


def show_current_process_status(remapper) -> None:
    """Показать текущий статус процесса в реальном времени."""
    if not remapper.process_monitor.get_active_window_process():
        print("❌ Библиотеки для определения процесса не установлены!")
        return

    print("\n🖥️  Текущий статус процесса:")
    print("Нажмите Ctrl+C для возврата в меню")

    try:
        while True:
            current_process = remapper.process_monitor.get_active_window_process()
            current_profile = remapper.config_manager.get_current_profile()
            is_target = remapper.process_monitor.is_target_process_active(
                current_profile.target_process,
                use_cache=False
            )

            status_icon = "✅" if is_target else "❌"
            print(
                f"\r{status_icon} Активный процесс: {current_process or 'Не определен'} | "
                f"Целевой: {current_profile.target_process} | "
                f"Работает: {'ДА' if is_target else 'НЕТ'}",
                end="", flush=True
            )
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n\n🔙 Возврат в меню...")