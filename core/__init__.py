"""
Основные модули приложения.
"""

# Ленивая загрузка для избежания циклических импортов

def __getattr__(name):
    if name == 'KeyboardRemapper':
        from .remapper import KeyboardRemapper
        return KeyboardRemapper
    elif name == 'ConfigManager':
        from .config_manager import ConfigManager
        return ConfigManager
    elif name == 'ProcessMonitor':
        from .process_monitor import ProcessMonitor
        return ProcessMonitor
    elif name == 'ActionExecutor':
        from .action_executor import ActionExecutor
        return ActionExecutor
    else:
        raise AttributeError(f"module 'core' has no attribute '{name}'")


