# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('constants.py', '.'),
        ('core/*.py', 'core'),
        ('ui/*.py', 'ui'),
        ('models/*.py', 'models'),
        ('utils/*.py', 'utils'),
    ],
    hiddenimports=[
        'win32gui',
        'win32process',
        'psutil',
        'pyperclip',
        'keyboard',
        'core.remapper',
        'core.config_manager',
        'core.process_monitor',
        'core.action_executor',
        'ui.menus',
        'ui.dialogs',
        'ui.display',
        'models.profile',
        'models.mapping',
        'utils.validators',
        'utils.formatters',
        'utils.helpers',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KeyboardRemapper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Сжатие для уменьшения размера
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Оставить True для отладки
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)