"""
Пользовательский интерфейс приложения.
"""

from .menus import main_menu, manage_profiles_menu
from .dialogs import (
    add_mapping_dialog, edit_mapping_dialog, remove_mapping_dialog,
    test_mapping_dialog, search_mappings_dialog
)
from .advanced_dialogs import (
    backup_management_dialog, macro_recording_dialog, quick_profile_dialog,
    settings_dialog
)

__all__ = [
    'main_menu', 'manage_profiles_menu', 'add_mapping_dialog',
    'edit_mapping_dialog', 'remove_mapping_dialog', 'test_mapping_dialog',
    'search_mappings_dialog', 'backup_management_dialog',
    'macro_recording_dialog', 'quick_profile_dialog', 'settings_dialog'
]