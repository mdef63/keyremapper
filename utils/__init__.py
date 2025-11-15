"""
Вспомогательные утилиты приложения.
"""

from .validators import validate_key, safe_input
from .formatters import format_key_display, get_action_display
from .helpers import clear_screen, input_multiline_text
from .backup_manager import BackupManager
from .macro_recorder import MacroRecorder

"""
Вспомогательные утилиты приложения.
"""

# Импорты будут выполнены только при обращении, чтобы избежать циклических импортов

def __getattr__(name):
    """Ленивая загрузка модулей для избежания циклических импортов."""
    if name == 'validate_key':
        from .validators import validate_key
        return validate_key
    elif name == 'safe_input':
        from .validators import safe_input
        return safe_input
    elif name == 'format_key_display':
        from .formatters import format_key_display
        return format_key_display
    elif name == 'get_action_display':
        from .formatters import get_action_display
        return get_action_display
    elif name == 'clear_screen':
        from .helpers import clear_screen
        return clear_screen
    elif name == 'input_multiline_text':
        from .helpers import input_multiline_text
        return input_multiline_text
    elif name == 'BackupManager':
        from .backup_manager import BackupManager
        return BackupManager
    elif name == 'MacroRecorder':
        from .macro_recorder import MacroRecorder
        return MacroRecorder
    else:
        raise AttributeError(f"module 'utils' has no attribute '{name}'")


__all__ = [
    'validate_key', 'safe_input', 'format_key_display',
    'get_action_display', 'clear_screen', 'input_multiline_text',
    'BackupManager', 'MacroRecorder'
]