"""
Диалоги и ввод для приложения переназначения клавиш.
"""

import os
import json
from typing import Optional, List

from utils.validators import validate_key, safe_input
from utils.helpers import input_multiline_text, select_symbol_from_category, select_currency
from utils.formatters import format_key_display, get_action_display


def add_mapping_dialog(remapper) -> None:
    """Диалог добавления назначения."""
    print("\n🎹 Поддерживаемые клавиши:")
    print("  • Функциональные: F1-F24")
    print("  • Буквы: a-z")
    print("  • Цифры: 0-9")
    print("  • Специальные: space, enter, tab, backspace, delete, esc, up, down, left, right, etc.")
    print("  • Комбинации: ctrl+a, alt+f4, shift+f1, win+r, ctrl+shift+a, etc.")
    print("\n💡 Примеры: F1, a, 5, space, ctrl+c, alt+tab, shift+f1, ctrl+shift+s")

    key = input("\nВведите клавишу или комбинацию: ").strip()
    validated_key = validate_key(key)

    if not validated_key:
        print("❌ Неверный формат клавиши!")
        return

    action = select_action_dialog()
    if not action:
        return

    # Проверка на дубликаты
    if validated_key in remapper.mappings:
        if not confirm_overwrite_dialog(validated_key, remapper.mappings[validated_key], action):
            return

    remapper.mappings[validated_key] = action
    remapper.config_manager.get_current_profile().mappings = remapper.mappings
    remapper.save_config(show_message=False)
    show_mapping_added_message(validated_key, action)


def select_action_dialog() -> Optional[str]:
    """Диалог выбора действия."""
    print("\n📝 Выберите действие:")
    print("1. Текст (одна строка)")
    print("2. Многострочный текст")
    print("3. Дата (длинный формат)")
    print("4. Дата (короткий формат)")
    print("5. Дата и время")
    print("6. Время")
    print("7. Символ валюты")
    print("8. ASCII символ")
    print("9. Комбинация клавиш")

    choice = input("Ваш выбор (1-9): ").strip()

    action_handlers = {
        '1': get_text_action,
        '2': get_multiline_text_action,
        '3': lambda: "date_long",
        '4': lambda: "date_short",
        '5': lambda: "datetime",
        '6': lambda: "time",
        '7': get_currency_action,
        '8': get_symbol_action,
        '9': get_key_combo_action
    }

    handler = action_handlers.get(choice)
    return handler() if handler else None


def get_text_action() -> str:
    """Получить действие для текста."""
    text = input('Введите текст в кавычках (например, "Привет мир"): ').strip()
    return f'"{text}"' if not (text.startswith('"') and text.endswith('"')) else text


def get_multiline_text_action() -> Optional[str]:
    """Получить действие для многострочного текста."""
    multiline_text = input_multiline_text()
    return f'"""{multiline_text}"""' if multiline_text else None


def get_currency_action() -> Optional[str]:
    """Получить действие для валюты."""
    currency_id = select_currency()
    return f"currency:{currency_id}" if currency_id else None


def get_symbol_action() -> Optional[str]:
    """Получить действие для символа."""
    symbol_id = select_symbol_from_category()
    return f"symbol:{symbol_id}" if symbol_id else None


def get_key_combo_action() -> str:
    """Получить действие для комбинации клавиш."""
    return input("Введите комбинацию (например, ctrl+c): ").strip()


def confirm_overwrite_dialog(key: str, old_action: str, new_action: str) -> bool:
    """Диалог подтверждения перезаписи."""
    display_key = format_key_display(key)
    old_display = get_action_display(old_action)
    new_display = get_action_display(new_action)

    overwrite = input(
        f"⚠️  Клавиша {display_key} уже назначена на: {old_display}\n"
        f"Перезаписать на: {new_display}? (y/n): "
    ).strip().lower()

    return overwrite == 'y'


def show_mapping_added_message(key: str, action: str) -> None:
    """Показать сообщение о добавлении маппинга."""
    display_key = format_key_display(key)

    if action.startswith('"""') and action.endswith('"""'):
        text_preview = action[3:-3]
        if len(text_preview) > 50:
            text_preview = text_preview[:50] + "..."
        print(f"✅ Назначение добавлено: {display_key} → Многострочный текст")
        print(f"   Предпросмотр: {text_preview}")
    else:
        display_action = get_action_display(action)
        print(f"✅ Назначение добавлено: {display_key} → {display_action}")


def edit_mapping_dialog(remapper) -> None:
    """Диалог редактирования назначения."""
    if not remapper.mappings:
        print("❌ Нет назначений для редактирования")
        return

    print("\n✏️  Редактирование назначения")
    keys = list(remapper.mappings.keys())
    for i, key in enumerate(keys, 1):
        action = remapper.mappings[key]
        display_action = get_action_display(action)
        display_key = format_key_display(key)
        print(f"  {i}. {display_key} → {display_action}")

    try:
        choice = int(input("\nВыберите номер для редактирования: ")) - 1
        if 0 <= choice < len(keys):
            key = keys[choice]
            old_action = remapper.mappings[key]

            print(f"\nТекущее действие: {get_action_display(old_action)}")
            new_action = select_action_dialog()

            if new_action:
                remapper.mappings[key] = new_action
                remapper.config_manager.get_current_profile().mappings = remapper.mappings
                remapper.save_config(show_message=False)
                display_key = format_key_display(key)
                print(f"✅ Назначение {display_key} обновлено → {get_action_display(new_action)}")
        else:
            print("❌ Неверный номер")
    except ValueError:
        print("❌ Введите число")


def remove_mapping_dialog(remapper) -> None:
    """Диалог удаления назначения."""
    if not remapper.mappings:
        print("❌ Нет назначений для удаления")
        return

    print("\n📝 Текущие назначения:")
    keys = list(remapper.mappings.keys())
    for i, key in enumerate(keys, 1):
        action = remapper.mappings[key]
        display_action = get_action_display(action)
        display_key = format_key_display(key)
        print(f"  {i}. {display_key} → {display_action}")

    print("\n💡 Введите номер для удаления, или несколько номеров через запятую (например: 1,3,5)")
    choice = input("Ваш выбор: ").strip()

    try:
        if ',' in choice:
            # Множественное удаление
            numbers = [int(x.strip()) - 1 for x in choice.split(',')]
            numbers = [n for n in numbers if 0 <= n < len(keys)]

            if not numbers:
                print("❌ Неверные номера")
                return

            removed_keys = []
            for num in sorted(numbers, reverse=True):
                key = keys[num]
                removed_keys.append(key)
                del remapper.mappings[key]

            remapper.config_manager.get_current_profile().mappings = remapper.mappings
            if remapper.save_config(create_backup=False):
                for key in removed_keys:
                    display_key = format_key_display(key)
                    print(f"✅ Назначение {display_key} удалено")
        else:
            # Одиночное удаление
            choice_num = int(choice) - 1
            if 0 <= choice_num < len(keys):
                key = keys[choice_num]
                del remapper.mappings[key]
                remapper.config_manager.get_current_profile().mappings = remapper.mappings
                if remapper.save_config(create_backup=False):
                    display_key = format_key_display(key)
                    print(f"✅ Назначение {display_key} удалено")
            else:
                print("❌ Неверный номер")
    except ValueError:
        print("❌ Введите число или числа через запятую")


def test_mapping_dialog(remapper) -> None:
    """Диалог тестирования назначения."""
    if not remapper.mappings:
        print("❌ Нет назначений для тестирования")
        return

    print("\n🧪 Тестирование назначения")
    keys = list(remapper.mappings.keys())
    for i, key in enumerate(keys, 1):
        action = remapper.mappings[key]
        display_action = get_action_display(action)
        display_key = format_key_display(key)
        print(f"  {i}. {display_key} → {display_action}")

    try:
        choice = int(input("\nВыберите номер для тестирования: ")) - 1
        if 0 <= choice < len(keys):
            key = keys[choice]
            action = remapper.mappings[key]
            display_key = format_key_display(key)
            display_action = get_action_display(action)

            print(f"\n🧪 Тестирование: {display_key} → {display_action}")
            print("💡 Откройте текстовый редактор и нажмите Enter для выполнения...")
            input("Нажмите Enter когда будете готовы: ")

            try:
                remapper.action_executor.execute_action(action)
                print("✅ Действие выполнено!")
            except Exception as e:
                print(f"❌ Ошибка при выполнении: {e}")
        else:
            print("❌ Неверный номер")
    except ValueError:
        print("❌ Введите число")


def search_mappings_dialog(remapper) -> None:
    """Диалог поиска назначений."""
    if not remapper.mappings:
        print("📝 Нет назначений для поиска")
        return []

    search_term = input("Введите поисковый запрос: ").strip().lower()
    if not search_term:
        return []

    results = []
    search_terms = search_term.split()

    for key, action in remapper.mappings.items():
        display_key = format_key_display(key)
        display_action = get_action_display(action)

        # Ищем в ключе, действии и тексте
        search_text = f"{display_key} {display_action}".lower()

        # Если несколько слов - все должны быть найдены
        if all(term in search_text for term in search_terms):
            results.append((key, action))

    if results:
        print(f"\n🔍 Найдено {len(results)} назначений:")
        for i, (key, action) in enumerate(results, 1):
            display_key = format_key_display(key)
            display_action = get_action_display(action)
            print(f"  {i}. {display_key} → {display_action}")
    else:
        print("❌ Ничего не найдено")

    return results


# Профильные диалоги (заглушки)
def list_profiles_dialog(remapper) -> None:
    """Диалог списка профилей."""
    remapper.config_manager.list_profiles()


def create_profile_dialog(remapper) -> None:
    """Диалог создания профиля."""
    print("\n➕ Создание нового профиля")
    name = input("Введите имя профиля: ").strip()

    if not name:
        print("❌ Имя профиля не может быть пустым")
        return

    if name in remapper.config_manager.profiles:
        print(f"❌ Профиль '{name}' уже существует")
        return

    # Создаем новый профиль
    from models.profile import Profile
    new_profile = Profile(name=name, mappings={}, target_process="Yandex")

    # Предлагаем скопировать настройки из текущего профиля
    if remapper.mappings:
        copy_choice = input(f"Скопировать настройки из текущего профиля '{remapper.config_manager.current_profile_name}'? (y/n): ").strip().lower()
        if copy_choice == 'y':
            new_profile.mappings = remapper.mappings.copy()
            new_profile.target_process = remapper.config_manager.get_current_profile().target_process

    remapper.config_manager.profiles[name] = new_profile
    if remapper.config_manager.save_config():
        print(f"✅ Профиль '{name}' создан")


def switch_profile_dialog(remapper) -> None:
    """Диалог переключения профиля."""
    if len(remapper.config_manager.profiles) <= 1:
        print("❌ Нет других профилей для переключения")
        return

    print("\n🔄 Переключение профиля")
    remapper.config_manager.list_profiles()

    profile_names = sorted(remapper.config_manager.profiles.keys())
    print("\nДоступные профили:")
    for i, profile_name in enumerate(profile_names, 1):
        marker = "👉" if profile_name == remapper.config_manager.current_profile_name else "  "
        print(f"{marker} {i}. {profile_name}")

    try:
        choice = input(f"\nВыберите профиль (1-{len(profile_names)}) или введите имя: ").strip()

        # Пытаемся как число
        try:
            num = int(choice)
            if 1 <= num <= len(profile_names):
                selected_profile = profile_names[num - 1]
            else:
                print("❌ Неверный номер")
                return
        except ValueError:
            # Или как имя
            selected_profile = choice
            if selected_profile not in remapper.config_manager.profiles:
                print(f"❌ Профиль '{selected_profile}' не найден")
                return

        if selected_profile == remapper.config_manager.current_profile_name:
            print("ℹ️  Этот профиль уже активен")
            return

        # Сохраняем текущий профиль
        current_profile = remapper.config_manager.get_current_profile()
        current_profile.mappings = remapper.mappings

        # Переключаемся
        remapper.config_manager.current_profile_name = selected_profile
        new_profile = remapper.config_manager.get_current_profile()
        remapper.mappings = new_profile.mappings

        if remapper.config_manager.save_config(create_backup=False):
            print(f"✅ Переключено на профиль '{selected_profile}'")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def duplicate_profile_dialog(remapper) -> None:
    """Диалог дублирования профиля."""
    print("\n📋 Дублирование профиля")
    remapper.config_manager.list_profiles()

    profile_names = sorted(remapper.config_manager.profiles.keys())
    print("\nДоступные профили:")
    for i, profile_name in enumerate(profile_names, 1):
        marker = "👉" if profile_name == remapper.config_manager.current_profile_name else "  "
        print(f"{marker} {i}. {profile_name}")

    try:
        choice = input(f"\nВыберите профиль для дублирования (1-{len(profile_names)}): ").strip()
        num = int(choice)
        if 1 <= num <= len(profile_names):
            source_profile_name = profile_names[num - 1]
            new_name = input(f"Введите имя для копии профиля '{source_profile_name}': ").strip()

            if not new_name:
                print("❌ Имя не может быть пустым")
                return

            if new_name in remapper.config_manager.profiles:
                print(f"❌ Профиль '{new_name}' уже существует")
                return

            # Копируем профиль
            import copy
            source_profile = remapper.config_manager.profiles[source_profile_name]
            new_profile = copy.deepcopy(source_profile)
            new_profile.name = new_name

            remapper.config_manager.profiles[new_name] = new_profile

            if remapper.config_manager.save_config():
                print(f"✅ Профиль '{source_profile_name}' скопирован в '{new_name}'")
        else:
            print("❌ Неверный номер")
    except ValueError:
        print("❌ Введите число")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def rename_profile_dialog(remapper) -> None:
    """Диалог переименования профиля."""
    print("\n✏️  Переименование профиля")
    remapper.config_manager.list_profiles()

    profile_names = sorted(remapper.config_manager.profiles.keys())
    print("\nДоступные профили:")
    for i, profile_name in enumerate(profile_names, 1):
        marker = "👉" if profile_name == remapper.config_manager.current_profile_name else "  "
        print(f"{marker} {i}. {profile_name}")

    try:
        choice = input(f"\nВыберите профиль для переименования (1-{len(profile_names)}): ").strip()
        num = int(choice)
        if 1 <= num <= len(profile_names):
            old_name = profile_names[num - 1]
            new_name = input(f"Введите новое имя для профиля '{old_name}': ").strip()

            if not new_name:
                print("❌ Имя не может быть пустым")
                return

            if new_name in remapper.config_manager.profiles:
                print(f"❌ Профиль '{new_name}' уже существует")
                return

            # Переименовываем
            profile = remapper.config_manager.profiles[old_name]
            profile.name = new_name
            remapper.config_manager.profiles[new_name] = profile
            del remapper.config_manager.profiles[old_name]

            # Обновляем текущий профиль, если он был переименован
            if remapper.config_manager.current_profile_name == old_name:
                remapper.config_manager.current_profile_name = new_name

            if remapper.config_manager.save_config():
                print(f"✅ Профиль '{old_name}' переименован в '{new_name}'")
        else:
            print("❌ Неверный номер")
    except ValueError:
        print("❌ Введите число")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def delete_profile_dialog(remapper) -> None:
    """Диалог удаления профиля."""
    if len(remapper.config_manager.profiles) <= 1:
        print("❌ Нельзя удалить последний профиль")
        return

    print("\n❌ Удаление профиля")
    remapper.config_manager.list_profiles()

    profile_names = sorted(remapper.config_manager.profiles.keys())
    print("\nДоступные профили:")
    for i, profile_name in enumerate(profile_names, 1):
        marker = "👉" if profile_name == remapper.config_manager.current_profile_name else "  "
        print(f"{marker} {i}. {profile_name}")

    try:
        choice = input(f"\nВыберите профиль для удаления (1-{len(profile_names)}): ").strip()
        num = int(choice)
        if 1 <= num <= len(profile_names):
            profile_to_delete = profile_names[num - 1]

            if profile_to_delete == remapper.config_manager.current_profile_name:
                print("❌ Нельзя удалить активный профиль")
                print("💡 Сначала переключитесь на другой профиль")
                return

            confirm = input(f"Удалить профиль '{profile_to_delete}'? (y/n): ").strip().lower()
            if confirm == 'y':
                del remapper.config_manager.profiles[profile_to_delete]
                if remapper.config_manager.save_config():
                    print(f"✅ Профиль '{profile_to_delete}' удален")
            else:
                print("❌ Отменено")
        else:
            print("❌ Неверный номер")
    except ValueError:
        print("❌ Введите число")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def change_target_process_dialog(remapper) -> None:
    """Диалог изменения целевого процесса."""
    current_profile = remapper.config_manager.get_current_profile()
    print(f"\n⚙️  Изменение целевого процесса")
    print(f"Текущий процесс: {current_profile.target_process}")
    print(f"Текущий профиль: {current_profile.name}")

    new_process = input("Введите имя процесса (или Enter для отмены): ").strip()
    if new_process:
        current_profile.target_process = new_process
        remapper.config_manager.save_config()
        print(f"✅ Целевой процесс изменен на: {new_process}")
    else:
        print("❌ Отменено")


def detect_current_process_dialog(remapper) -> None:
    """Диалог определения текущего процесса."""
    if not remapper.process_monitor.get_active_window_process():
        print("❌ Библиотеки для определения процесса не установлены!")
        return

    print("\n🔍 Определение текущего активного процесса...")
    print("💡 Переключитесь на нужное окно и нажмите Enter")
    input("Нажмите Enter когда окно будет активно: ")

    current_process = remapper.process_monitor.get_active_window_process()
    if current_process:
        print(f"\n📌 Обнаружен процесс: {current_process}")
        use_it = input(f"Использовать '{current_process}' как целевой процесс? (y/n): ").strip().lower()
        if use_it == 'y':
            current_profile = remapper.config_manager.get_current_profile()
            current_profile.target_process = current_process
            remapper.config_manager.save_config()
            print(f"✅ Целевой процесс установлен: {current_process}")
        else:
            print("❌ Отменено")
    else:
        print("❌ Не удалось определить активный процесс")


def export_profile_dialog(remapper) -> None:
    """Диалог экспорта профиля."""
    print("💾 Экспорт профиля - функция в разработке")


def import_profile_dialog(remapper) -> None:
    """Диалог импорта профиля."""
    print("📥 Импорт профиля - функция в разработке")


def show_statistics_dialog(remapper) -> None:
    """Диалог показа статистики."""
    print("\n📊 СТАТИСТИКА")
    print("=" * 50)
    print(f"Всего профилей: {len(remapper.config_manager.profiles)}")

    total_mappings = sum(len(profile.mappings) for profile in remapper.config_manager.profiles.values())
    print(f"Всего назначений: {total_mappings}")

    current_profile = remapper.config_manager.get_current_profile()
    print(f"Текущий профиль: {current_profile.name} ({len(current_profile.mappings)} назначений)")

    # Статистика по типам действий
    action_types = {}
    for action in remapper.mappings.values():
        if action in ["date_long", "date_short", "datetime", "time"]:
            action_types['Дата/Время'] = action_types.get('Дата/Время', 0) + 1
        elif action.startswith('currency:'):
            action_types['Валюты'] = action_types.get('Валюты', 0) + 1
        elif action.startswith('symbol:'):
            action_types['Символы'] = action_types.get('Символы', 0) + 1
        elif action.startswith('"""'):
            action_types['Многострочный текст'] = action_types.get('Многострочный текст', 0) + 1
        elif action.startswith('"'):
            action_types['Текст'] = action_types.get('Текст', 0) + 1
        else:
            action_types['Клавиши'] = action_types.get('Клавиши', 0) + 1

    if action_types:
        print("\n📈 Распределение по типам действий:")
        for action_type, count in sorted(action_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {action_type}: {count}")

    print("\n📋 Детали по профилям:")
    for profile_name, profile in remapper.config_manager.profiles.items():
        marker = "👉" if profile_name == remapper.config_manager.current_profile_name else "  "
        print(f"{marker} {profile_name}: {len(profile.mappings)} назначений, процесс: {profile.target_process}")


def show_info_dialog() -> None:
    """Диалог показа информации о программе."""
    print("\n📊 ИНФОРМАЦИЯ О ПРОГРАММЕ")
    print("=" * 30)
    print("🎹 Переназначение клавиш")
    print("📝 Поддерживаемые клавиши:")
    print("  • Функциональные: F1-F24")
    print("  • Буквы: a-z")
    print("  • Цифры: 0-9")
    print("  • Специальные: space, enter, tab, backspace, delete, esc, etc.")
    print("  • Комбинации: ctrl+a, alt+f4, shift+f1, win+r, ctrl+shift+a, etc.")
    print("\n📝 Возможности:")
    print("  • Вставка русского текста (одна строка)")
    print("  • Вставка многострочного текста (с поддержкой пустых строк)")
    print("  • Вставка текущей даты и времени")
    print("  • Запуск комбинаций клавиш")
    print("  • Автосохранение настроек")
    print("  • Работа только для указанного процесса")
    print("  • Профили для разных наборов настроек")