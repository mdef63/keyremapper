"""
Продвинутые диалоги для новых функций.
"""

import os
import time
from typing import List, Optional, Dict, Any

from utils.backup_manager import BackupManager
from utils.macro_recorder import MacroRecorder
from utils.macro_manager import MacroManager
from utils.profile_templates import list_quick_profile_templates, get_quick_profile_template
from core.settings_manager import SettingsManager, AutoStartManager
from utils.formatters import format_key_display
from utils.helpers import clear_screen
from models.mapping import Macro
from models.profile import Profile


def backup_management_dialog(remapper) -> None:
    """Диалог управления резервными копиями."""
    backup_manager = BackupManager()

    while True:
        clear_screen()
        print("\n" + "=" * 50)
        print("💾 УПРАВЛЕНИЕ РЕЗЕРВНЫМИ КОПИЯМИ")
        print("=" * 50)

        backups = backup_manager.list_backups()
        print(f"📂 Найдено резервных копий: {len(backups)}")

        print("\n1. 📋 Список резервных копий")
        print("2. 💾 Создать резервную копию")
        print("3. 📦 Создать полный backup (ZIP)")
        print("4. 🔄 Восстановить из резервной копии")
        print("5. 🗑️  Удалить резервную копию")
        print("6. 🧹 Очистить старые резервные копии")
        print("7. ℹ️  Информация о резервной копии")
        print("0. 🔙 Назад")

        choice = input("\n🎯 Выберите действие: ").strip()

        if choice == '1':
            list_backups_dialog(backup_manager)
        elif choice == '2':
            create_backup_dialog(backup_manager)
        elif choice == '3':
            create_zip_backup_dialog(backup_manager)
        elif choice == '4':
            restore_backup_dialog(backup_manager, remapper)
        elif choice == '5':
            delete_backup_dialog(backup_manager)
        elif choice == '6':
            cleanup_backups_dialog(backup_manager)
        elif choice == '7':
            backup_info_dialog(backup_manager)
        elif choice == '0':
            break
        else:
            print("❌ Неверный выбор")
            input("Нажмите Enter для продолжения...")


def list_backups_dialog(backup_manager: BackupManager) -> None:
    """Диалог списка резервных копий."""
    backups = backup_manager.list_backups()

    if not backups:
        print("📝 Резервные копии не найдены")
        input("Нажмите Enter для продолжения...")
        return

    print(f"\n📋 Найдено резервных копий: {len(backups)}")
    for i, backup in enumerate(backups, 1):
        size_kb = backup['size'] / 1024
        desc = backup['description']
        created = backup['created'].strftime('%d.%m.%Y %H:%M')
        print(f"{i}. {backup['name']} ({size_kb:.1f} KB) - {created} - {desc}")

    input("\nНажмите Enter для продолжения...")


def create_backup_dialog(backup_manager: BackupManager) -> None:
    """Диалог создания резервной копии."""
    description = input("Введите описание резервной копии (опционально): ").strip()

    backup_path = backup_manager.create_backup(description)
    if not backup_path:
        print("❌ Не удалось создать резервную копию")

    input("Нажмите Enter для продолжения...")


def create_zip_backup_dialog(backup_manager: BackupManager) -> None:
    """Диалог создания ZIP-архива."""
    include_logs = input("Включить логи в архив? (y/n): ").strip().lower() == 'y'

    zip_path = backup_manager.create_zip_backup(include_logs=include_logs)
    if not zip_path:
        print("❌ Не удалось создать ZIP-архив")

    input("Нажмите Enter для продолжения...")


def restore_backup_dialog(backup_manager: BackupManager, remapper) -> None:
    """Диалог восстановления из резервной копии."""
    backups = backup_manager.list_backups()

    if not backups:
        print("📝 Резервные копии не найдены")
        input("Нажмите Enter для продолжения...")
        return

    print("\n📋 Доступные резервные копии:")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup['name']} - {backup['created'].strftime('%d.%m.%Y %H:%M')}")

    try:
        choice = int(input("\nВыберите номер для восстановления: ").strip())
        if 1 <= choice <= len(backups):
            backup = backups[choice - 1]
            confirm = input(f"Восстановить конфигурацию из {backup['name']}? (y/n): ").strip().lower()
            if confirm == 'y':
                if backup_manager.restore_backup(backup['path']):
                    print("🔄 Перезагружаем конфигурацию...")
                    remapper.load_config()
                    print("✅ Конфигурация перезагружена")
                else:
                    print("❌ Ошибка восстановления")
        else:
            print("❌ Неверный номер")
    except ValueError:
        print("❌ Введите число")

    input("Нажмите Enter для продолжения...")


def delete_backup_dialog(backup_manager: BackupManager) -> None:
    """Диалог удаления резервной копии."""
    backups = backup_manager.list_backups()

    if not backups:
        print("📝 Резервные копии не найдены")
        input("Нажмите Enter для продолжения...")
        return

    print("\n📋 Доступные резервные копии:")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup['name']} - {backup['created'].strftime('%d.%m.%Y %H:%M')}")

    try:
        choice = int(input("\nВыберите номер для удаления: ").strip())
        if 1 <= choice <= len(backups):
            backup = backups[choice - 1]
            confirm = input(f"Удалить резервную копию {backup['name']}? (y/n): ").strip().lower()
            if confirm == 'y':
                if not backup_manager.delete_backup(backup['path']):
                    print("❌ Ошибка удаления")
        else:
            print("❌ Неверный номер")
    except ValueError:
        print("❌ Введите число")

    input("Нажмите Enter для продолжения...")


def cleanup_backups_dialog(backup_manager: BackupManager) -> None:
    """Диалог очистки резервных копий."""
    backups = backup_manager.list_backups()

    if len(backups) <= backup_manager.max_backups:
        print("✅ Нет старых резервных копий для очистки")
        input("Нажмите Enter для продолжения...")
        return

    print(f"🗑️  Будут удалены {len(backups) - backup_manager.max_backups} старых резервных копий")
    confirm = input("Продолжить? (y/n): ").strip().lower()

    if confirm == 'y':
        backup_manager._cleanup_old_backups()
        print("✅ Старые резервные копии удалены")

    input("Нажмите Enter для продолжения...")


def backup_info_dialog(backup_manager: BackupManager) -> None:
    """Диалог информации о резервной копии."""
    backups = backup_manager.list_backups()

    if not backups:
        print("📝 Резервные копии не найдены")
        input("Нажмите Enter для продолжения...")
        return

    print("\n📋 Доступные резервные копии:")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup['name']} - {backup['created'].strftime('%d.%m.%Y %H:%M')}")

    try:
        choice = int(input("\nВыберите номер для просмотра информации: ").strip())
        if 1 <= choice <= len(backups):
            backup = backups[choice - 1]
            info = backup_manager.get_backup_info(backup['path'])
            if info:
                print(f"\nℹ️  Информация о {backup['name']}:")
                print(f"   Тип: {info.get('type', 'Неизвестно')}")
                if 'profile_count' in info:
                    print(f"   Профилей: {info['profile_count']}")
                if 'current_profile' in info:
                    print(f"   Текущий профиль: {info['current_profile']}")
            else:
                print("❌ Не удалось получить информацию о резервной копии")
        else:
            print("❌ Неверный номер")
    except ValueError:
        print("❌ Введите число")

    input("Нажмите Enter для продолжения...")


def macro_recording_dialog(remapper) -> None:
    """Диалог записи макросов."""
    recorder = MacroRecorder()
    macro_manager = MacroManager(remapper.config_manager)

    while True:
        clear_screen()
        print("\n🎙️  ЗАПИСЬ МАКРОСОВ")
        print("=" * 30)
        print("1. 🔴 Начать запись макроса")
        print("2. 📋 Список макросов")
        print("3. ▶️  Выполнить макрос")
        print("4. ➕ Создать макрос вручную")
        print("5. 🗑️  Удалить макрос")
        print("6. 📥 Импорт макросов из назначений")
        print("0. 🔙 Назад")

        choice = input("\n🎯 Выберите действие: ").strip()

        if choice == '1':
            start_macro_recording(recorder, macro_manager)
        elif choice == '2':
            list_macros_dialog(macro_manager)
        elif choice == '3':
            execute_macro_dialog(macro_manager, remapper.action_executor)
        elif choice == '4':
            create_manual_macro_dialog(macro_manager)
        elif choice == '5':
            delete_macro_dialog(macro_manager)
        elif choice == '6':
            import_macros_dialog(macro_manager, remapper.mappings)
        elif choice == '0':
            break
        else:
            print("❌ Неверный выбор")
            input("Нажмите Enter для продолжения...")


def start_macro_recording(recorder: MacroRecorder, macro_manager: MacroManager) -> None:
    """Начинает запись макроса."""
    if recorder.start_recording():
        print("🔴 Запись начата...")
        print("💡 Нажимайте клавиши для записи макроса")
        print("⏹️  Для остановки нажмите F12")

        # Ждем завершения записи
        try:
            import keyboard
            keyboard.wait('f12')
        except KeyboardInterrupt:
            pass

        events = recorder.stop_recording()
        if events:
            print(f"✅ Записано {len(events)} событий")
            save_recorded_macro_dialog(events, macro_manager)
        else:
            print("❌ Не было записано ни одного события")
    else:
        print("❌ Не удалось начать запись")

    input("Нажмите Enter для продолжения...")


def save_recorded_macro_dialog(events: List[Dict], macro_manager: MacroManager) -> None:
    """Диалог сохранения записанного макроса."""
    if not events:
        return

    macro_name = input("Введите имя для макроса: ").strip()
    if not macro_name:
        print("❌ Имя макроса не может быть пустым")
        return

    description = input("Введите описание макроса (опционально): ").strip()

    # Конвертируем события в макрос
    macro = recorder.convert_to_mapping(events, macro_name)
    if macro:
        macro.description = description
        if macro_manager.create_macro(macro.name, macro.action_type, macro.value, macro.description):
            print(f"✅ Макрос '{macro_name}' сохранен")
        else:
            print("❌ Ошибка сохранения макроса")
    else:
        print("❌ Не удалось создать макрос из записанных событий")


def list_macros_dialog(macro_manager: MacroManager) -> None:
    """Диалог списка макросов."""
    macros = macro_manager.list_macros()
    categories = macro_manager.get_categories()

    if not macros:
        print("📝 Макросы не найдены")
        input("Нажмите Enter для продолжения...")
        return

    print(f"\n📋 Найдено макросов: {len(macros)}")

    for category in categories:
        category_macros = macro_manager.list_macros(category)
        print(f"\n📁 {category} ({len(category_macros)}):")
        for macro in category_macros:
            print(f"  • {macro.name}: {macro.description}")

    input("\nНажмите Enter для продолжения...")


def execute_macro_dialog(macro_manager: MacroManager, executor) -> None:
    """Диалог выполнения макроса."""
    macros = macro_manager.list_macros()

    if not macros:
        print("📝 Макросы не найдены")
        input("Нажмите Enter для продолжения...")
        return

    print("\n📋 Доступные макросы:")
    for i, macro in enumerate(macros, 1):
        print(f"{i}. {macro.name} - {macro.description}")

    try:
        choice = int(input("\nВыберите макрос для выполнения: ").strip())
        if 1 <= choice <= len(macros):
            macro = macros[choice - 1]
            print(f"▶️  Выполнение макроса: {macro.name}")
            input("Нажмите Enter когда будете готовы...")

            if macro_manager.execute_macro(macro.name, executor):
                print("✅ Макрос выполнен")
            else:
                print("❌ Ошибка выполнения макроса")
        else:
            print("❌ Неверный номер")
    except ValueError:
        print("❌ Введите число")

    input("Нажмите Enter для продолжения...")


def create_manual_macro_dialog(macro_manager: MacroManager) -> None:
    """Диалог создания макроса вручную."""
    print("\n➕ Создание макроса вручную")

    name = input("Введите имя макроса: ").strip()
    if not name:
        print("❌ Имя макроса не может быть пустым")
        return

    if macro_manager.get_macro(name):
        print("❌ Макрос с таким именем уже существует")
        return

    print("\n📝 Выберите тип макроса:")
    print("1. Текст")
    print("2. Действие (дата, время, символ)")
    print("3. Комбинация клавиш")

    choice = input("Ваш выбор: ").strip()

    action_type = ""
    value = ""

    if choice == '1':
        action_type = "text"
        value = input("Введите текст: ").strip()
    elif choice == '2':
        action_type = "action"
        print("Доступные действия: date_long, date_short, datetime, time")
        print("Или символы: symbol:plus, symbol:arrow_left, etc.")
        value = input("Введите действие: ").strip()
    elif choice == '3':
        action_type = "key_combo"
        value = input("Введите комбинацию клавиш (например: ctrl+c): ").strip()
    else:
        print("❌ Неверный выбор")
        return

    description = input("Введите описание (опционально): ").strip()
    category = input("Введите категорию (опционально): ").strip() or "general"

    if macro_manager.create_macro(name, action_type, value, description, category):
        print(f"✅ Макрос '{name}' создан")
    else:
        print("❌ Ошибка создания макроса")

    input("Нажмите Enter для продолжения...")


def delete_macro_dialog(macro_manager: MacroManager) -> None:
    """Диалог удаления макроса."""
    macros = macro_manager.list_macros()

    if not macros:
        print("📝 Макросы не найдены")
        input("Нажмите Enter для продолжения...")
        return

    print("\n📋 Доступные макросы:")
    for i, macro in enumerate(macros, 1):
        print(f"{i}. {macro.name} - {macro.description}")

    try:
        choice = int(input("\nВыберите макрос для удаления: ").strip())
        if 1 <= choice <= len(macros):
            macro = macros[choice - 1]
            confirm = input(f"Удалить макрос '{macro.name}'? (y/n): ").strip().lower()
            if confirm == 'y':
                if macro_manager.delete_macro(macro.name):
                    print("✅ Макрос удален")
                else:
                    print("❌ Ошибка удаления макроса")
        else:
            print("❌ Неверный номер")
    except ValueError:
        print("❌ Введите число")

    input("Нажмите Enter для продолжения...")


def import_macros_dialog(macro_manager: MacroManager, mappings: Dict[str, str]) -> None:
    """Диалог импорта макросов из назначений."""
    if not mappings:
        print("📝 Нет назначений для импорта")
        input("Нажмите Enter для продолжения...")
        return

    print(f"📥 Импорт макросов из {len(mappings)} назначений")
    confirm = input("Продолжить? (y/n): ").strip().lower()

    if confirm == 'y':
        imported_count = macro_manager.import_macros_from_mappings(mappings)
        print(f"✅ Импортировано {imported_count} макросов")

    input("Нажмите Enter для продолжения...")


def quick_profile_dialog(remapper) -> None:
    """Диалог быстрых профилей."""
    templates = list_quick_profile_templates()

    while True:
        clear_screen()
        print("\n🚀 БЫСТРЫЕ ПРОФИЛИ")
        print("=" * 30)

        if not templates:
            print("📝 Шаблоны профилей не найдены")
            break

        for i, template in enumerate(templates, 1):
            print(f"{i}. {template['name']}")
            print(f"   {template['description']}")
            print(f"   🎯 Процесс: {template['target_process']}")
            print(f"   📝 Назначений: {template['mappings_count']}")
            print()

        print("0. 🔙 Назад")

        try:
            choice = int(input("\nВыберите шаблон профиля: ").strip())
            if choice == 0:
                break
            elif 1 <= choice <= len(templates):
                template = templates[choice - 1]
                create_quick_profile_from_template(remapper, template)
                break
            else:
                print("❌ Неверный номер")
                input("Нажмите Enter для продолжения...")
        except ValueError:
            print("❌ Введите число")
            input("Нажмите Enter для продолжения...")


def create_quick_profile_from_template(remapper, template: Dict[str, Any]) -> None:
    """Создает профиль из шаблона."""
    profile_name = input(f"Введите имя для профиля (Enter для '{template['name']}'): ").strip()
    if not profile_name:
        profile_name = template['name']

    # Проверяем, существует ли уже профиль с таким именем
    if profile_name in remapper.config_manager.profiles:
        overwrite = input(f"Профиль '{profile_name}' уже существует. Перезаписать? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("❌ Отменено")
            return

    # Получаем полный шаблон
    full_template = get_quick_profile_template(template['id'])
    if not full_template:
        print("❌ Ошибка загрузки шаблона")
        return

    # Создаем новый профиль
    new_profile = Profile(
        name=profile_name,
        mappings=full_template['preset_mappings'],
        target_process=full_template['target_process']
    )

    # Добавляем профиль в конфигурацию
    remapper.config_manager.profiles[profile_name] = new_profile

    # Переключаемся на новый профиль
    remapper.config_manager.current_profile_name = profile_name
    remapper.mappings = new_profile.mappings.copy()

    if remapper.save_config():
        print(f"✅ Профиль '{profile_name}' создан и активирован")
        print(f"🎯 Целевой процесс: {new_profile.target_process}")
        print(f"📝 Назначений: {len(new_profile.mappings)}")
    else:
        print("❌ Ошибка сохранения профиля")

    input("Нажмите Enter для продолжения...")


def settings_dialog(remapper) -> None:
    """Диалог настроек приложения."""
    settings_manager = SettingsManager()
    autostart_manager = AutoStartManager()

    while True:
        clear_screen()
        print("\n⚙️  НАСТРОЙКИ ПРИЛОЖЕНИЯ")
        print("=" * 30)

        # Текущие настройки
        settings = settings_manager.get_all_settings()
        autostart_enabled = autostart_manager.is_autostart_enabled()

        print("Текущие настройки:")
        print(f"  🔄 Автозагрузка: {'Включена' if autostart_enabled else 'Выключена'}")
        print(f"  ⏱️  Задержка печати: {settings['typing_delay']} сек")
        print(f"  💾 Авто-бэкап: {'Включен' if settings['auto_backup'] else 'Выключен'}")
        print(f"  🎨 Тема: {settings['theme']}")

        print("\n1. 🔄 Управление автозагрузкой")
        print("2. ⏱️  Настройки задержек")
        print("3. 💾 Настройки резервного копирования")
        print("4. 🎨 Настройки интерфейса")
        print("5. 🔧 Расширенные настройки")
        print("6. 🗑️  Сброс настроек")
        print("0. 🔙 Назад")

        choice = input("\nВыберите настройку: ").strip()

        if choice == '1':
            autostart_settings_dialog(autostart_manager)
        elif choice == '2':
            delay_settings_dialog(settings_manager)
        elif choice == '3':
            backup_settings_dialog(settings_manager)
        elif choice == '4':
            interface_settings_dialog(settings_manager)
        elif choice == '5':
            advanced_settings_dialog(settings_manager)
        elif choice == '6':
            reset_settings_dialog(settings_manager)
        elif choice == '0':
            break
        else:
            print("❌ Неверный выбор")
            input("Нажмите Enter для продолжения...")


def autostart_settings_dialog(autostart_manager: AutoStartManager) -> None:
    """Диалог настройки автозагрузки."""
    current_status = autostart_manager.is_autostart_enabled()

    print(f"\n🔄 АВТОЗАГРУЗКА: {'ВКЛЮЧЕНА' if current_status else 'ВЫКЛЮЧЕНА'}")
    print("=" * 30)

    if current_status:
        print("1. ❌ Выключить автозагрузку")
        print("2. 🔙 Назад")

        choice = input("\nВыберите действие: ").strip()
        if choice == '1':
            if autostart_manager.disable_autostart():
                print("✅ Автозагрузка выключена")
            else:
                print("❌ Ошибка выключения автозагрузки")
    else:
        print("1. ✅ Включить автозагрузку")
        print("2. 🔙 Назад")

        choice = input("\nВыберите действие: ").strip()
        if choice == '1':
            if autostart_manager.enable_autostart():
                print("✅ Автозагрузка включена")
            else:
                print("❌ Ошибка включения автозагрузки")

    input("Нажмите Enter для продолжения...")


def delay_settings_dialog(settings_manager: SettingsManager) -> None:
    """Диалог настройки задержек."""
    current_delay = settings_manager.get_setting('typing_delay')
    current_clipboard_timeout = settings_manager.get_setting('clipboard_timeout')
    current_process_check = settings_manager.get_setting('process_check_frequency')

    print(f"\n⏱️  ТЕКУЩИЕ ЗАДЕРЖКИ")
    print("=" * 30)
    print(f"Задержка печати: {current_delay} сек")
    print(f"Таймаут буфера обмена: {current_clipboard_timeout} сек")
    print(f"Частота проверки процессов: {current_process_check} сек")

    print("\n1. ✏️  Изменить задержку печати")
    print("2. ✏️  Изменить таймаут буфера обмена")
    print("3. ✏️  Изменить частоту проверки процессов")
    print("4. 🔙 Назад")

    choice = input("\nВыберите действие: ").strip()

    if choice == '1':
        new_delay = input(f"Введите новую задержку печати (текущая: {current_delay}): ").strip()
        try:
            new_delay_float = float(new_delay)
            if 0.001 <= new_delay_float <= 1.0:
                if settings_manager.set_setting('typing_delay', new_delay_float):
                    print("✅ Задержка печати изменена")
                else:
                    print("❌ Ошибка изменения настройки")
            else:
                print("❌ Задержка должна быть между 0.001 и 1.0 секунд")
        except ValueError:
            print("❌ Введите число")

    elif choice == '2':
        new_timeout = input(f"Введите новый таймаут буфера обмена (текущий: {current_clipboard_timeout}): ").strip()
        try:
            new_timeout_float = float(new_timeout)
            if 0.01 <= new_timeout_float <= 0.5:
                if settings_manager.set_setting('clipboard_timeout', new_timeout_float):
                    print("✅ Таймаут буфера обмена изменен")
                else:
                    print("❌ Ошибка изменения настройки")
            else:
                print("❌ Таймаут должен быть между 0.01 и 0.5 секунд")
        except ValueError:
            print("❌ Введите число")

    elif choice == '3':
        new_frequency = input(f"Введите новую частоту проверки процессов (текущая: {current_process_check}): ").strip()
        try:
            new_frequency_float = float(new_frequency)
            if 0.05 <= new_frequency_float <= 1.0:
                if settings_manager.set_setting('process_check_frequency', new_frequency_float):
                    print("✅ Частота проверки процессов изменена")
                else:
                    print("❌ Ошибка изменения настройки")
            else:
                print("❌ Частота должна быть между 0.05 и 1.0 секунд")
        except ValueError:
            print("❌ Введите число")

    input("Нажмите Enter для продолжения...")


def backup_settings_dialog(settings_manager: SettingsManager) -> None:
    """Диалог настроек резервного копирования."""
    auto_backup = settings_manager.get_setting('auto_backup')
    max_backups = settings_manager.get_setting('max_backup_files')
    backup_on_start = settings_manager.get_setting('backup_on_start')

    print(f"\n💾 НАСТРОЙКИ РЕЗЕРВНОГО КОПИРОВАНИЯ")
    print("=" * 30)
    print(f"Авто-бэкап: {'Включен' if auto_backup else 'Выключен'}")
    print(f"Максимум резервных копий: {max_backups}")
    print(f"Бэкап при запуске: {'Включен' if backup_on_start else 'Выключен'}")

    print("\n1. 🔄 Переключить авто-бэкап")
    print("2. ✏️  Изменить максимум резервных копий")
    print("3. 🔄 Переключить бэкап при запуске")
    print("4. 🔙 Назад")

    choice = input("\nВыберите действие: ").strip()

    if choice == '1':
        new_value = not auto_backup
        if settings_manager.set_setting('auto_backup', new_value):
            status = "включен" if new_value else "выключен"
            print(f"✅ Авто-бэкап {status}")
        else:
            print("❌ Ошибка изменения настройки")

    elif choice == '2':
        new_max = input(f"Введите новое максимальное количество резервных копий (текущее: {max_backups}): ").strip()
        try:
            new_max_int = int(new_max)
            if 1 <= new_max_int <= 100:
                if settings_manager.set_setting('max_backup_files', new_max_int):
                    print("✅ Максимум резервных копий изменен")
                else:
                    print("❌ Ошибка изменения настройки")
            else:
                print("❌ Количество должно быть между 1 и 100")
        except ValueError:
            print("❌ Введите число")

    elif choice == '3':
        new_value = not backup_on_start
        if settings_manager.set_setting('backup_on_start', new_value):
            status = "включен" if new_value else "выключен"
            print(f"✅ Бэкап при запуске {status}")
        else:
            print("❌ Ошибка изменения настройки")

    input("Нажмите Enter для продолжения...")


def interface_settings_dialog(settings_manager: SettingsManager) -> None:
    """Диалог настроек интерфейса."""
    show_notifications = settings_manager.get_setting('show_notifications')
    compact_mode = settings_manager.get_setting('compact_mode')
    theme = settings_manager.get_setting('theme')

    print(f"\n🎨 НАСТРОЙКИ ИНТЕРФЕЙСА")
    print("=" * 30)
    print(f"Показывать уведомления: {'Да' if show_notifications else 'Нет'}")
    print(f"Компактный режим: {'Да' if compact_mode else 'Нет'}")
    print(f"Тема: {theme}")

    print("\n1. 🔄 Переключить уведомления")
    print("2. 🔄 Переключить компактный режим")
    print("3. 🎨 Изменить тему")
    print("4. 🔙 Назад")

    choice = input("\nВыберите действие: ").strip()

    if choice == '1':
        new_value = not show_notifications
        if settings_manager.set_setting('show_notifications', new_value):
            status = "включены" if new_value else "выключены"
            print(f"✅ Уведомления {status}")
        else:
            print("❌ Ошибка изменения настройки")

    elif choice == '2':
        new_value = not compact_mode
        if settings_manager.set_setting('compact_mode', new_value):
            status = "включен" if new_value else "выключен"
            print(f"✅ Компактный режим {status}")
        else:
            print("❌ Ошибка изменения настройки")

    elif choice == '3':
        print("\nДоступные темы:")
        print("1. Стандартная")
        print("2. Темная")
        print("3. Светлая")

        theme_choice = input("Выберите тему: ").strip()
        themes = {'1': 'default', '2': 'dark', '3': 'light'}

        if theme_choice in themes:
            new_theme = themes[theme_choice]
            if settings_manager.set_setting('theme', new_theme):
                print(f"✅ Тема изменена на: {new_theme}")
            else:
                print("❌ Ошибка изменения настройки")
        else:
            print("❌ Неверный выбор")

    input("Нажмите Enter для продолжения...")


def advanced_settings_dialog(settings_manager: SettingsManager) -> None:
    """Диалог расширенных настроек."""
    debug_mode = settings_manager.get_setting('debug_mode')
    log_level = settings_manager.get_setting('log_level')
    start_minimized = settings_manager.get_setting('start_minimized')

    print(f"\n🔧 РАСШИРЕННЫЕ НАСТРОЙКИ")
    print("=" * 30)
    print(f"Режим отладки: {'Включен' if debug_mode else 'Выключен'}")
    print(f"Уровень логирования: {log_level}")
    print(f"Запуск свернутым: {'Да' if start_minimized else 'Нет'}")

    print("\n1. 🔄 Переключить режим отладки")
    print("2. 📊 Изменить уровень логирования")
    print("3. 🔄 Переключить запуск свернутым")
    print("4. 🔙 Назад")

    choice = input("\nВыберите действие: ").strip()

    if choice == '1':
        new_value = not debug_mode
        if settings_manager.set_setting('debug_mode', new_value):
            status = "включен" if new_value else "выключен"
            print(f"✅ Режим отладки {status}")
        else:
            print("❌ Ошибка изменения настройки")

    elif choice == '2':
        print("\nДоступные уровни логирования:")
        print("1. DEBUG - Подробная отладочная информация")
        print("2. INFO - Основная информация (рекомендуется)")
        print("3. WARNING - Только предупреждения и ошибки")
        print("4. ERROR - Только ошибки")

        level_choice = input("Выберите уровень: ").strip()
        levels = {'1': 'DEBUG', '2': 'INFO', '3': 'WARNING', '4': 'ERROR'}

        if level_choice in levels:
            new_level = levels[level_choice]
            if settings_manager.set_setting('log_level', new_level):
                print(f"✅ Уровень логирования изменен на: {new_level}")
            else:
                print("❌ Ошибка изменения настройки")
        else:
            print("❌ Неверный выбор")

    elif choice == '3':
        new_value = not start_minimized
        if settings_manager.set_setting('start_minimized', new_value):
            status = "включен" if new_value else "выключен"
            print(f"✅ Запуск свернутым {status}")
        else:
            print("❌ Ошибка изменения настройки")

    input("Нажмите Enter для продолжения...")


def reset_settings_dialog(settings_manager: SettingsManager) -> None:
    """Диалог сброса настроек."""
    print("\n🗑️  СБРОС НАСТРОЕК")
    print("=" * 30)
    print("⚠️  ВНИМАНИЕ: Это действие сбросит все настройки приложения")
    print("к значениям по умолчанию. Это действие нельзя отменить!")

    confirm = input("\nВы уверены? (введите 'СБРОС' для подтверждения): ").strip()

    if confirm == 'СБРОС':
        if settings_manager.reset_settings():
            print("✅ Настройки сброшены к значениям по умолчанию")
        else:
            print("❌ Ошибка сброса настроек")
    else:
        print("❌ Сброс отменен")

    input("Нажмите Enter для продолжения...")