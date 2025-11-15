"""
Модели данных приложения.
"""

# Используем ленивую загрузку для избежания циклических импортов

def __getattr__(name):
    """Ленивая загрузка модулей."""
    if name == 'Profile':
        from .profile import Profile
        return Profile
    elif name == 'KeyMapping':
        from .mapping import KeyMapping
        return KeyMapping
    elif name == 'ActionType':
        from .mapping import ActionType
        return ActionType
    elif name == 'AppSettings':
        from .settings import AppSettings
        return AppSettings
    elif name == 'Macro':
        from .mapping import Macro
        return Macro
    else:
        raise AttributeError(f"module 'models' has no attribute '{name}'")


