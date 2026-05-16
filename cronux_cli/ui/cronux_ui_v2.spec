# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

block_cipher = None

a = Analysis(
    ['cronux_ui_v2.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('screens', 'screens'),
        ('components', 'components'),
        ('cli', 'cli'),
        ('../assets', 'assets'),
    ],
    hiddenimports=[
        'flet',
        'flet.core',
        'flet.auth',
        'flet.controls',
        'cli_integration',
        'screens.home_screen',
        'screens.wizard_screen',
        'screens.project_screen_v2',
        'components.terminal_loader',
        'components.gradient_button',
        'components.loader',
        'components.project_type_card',
        # Módulos CLI
        'cli.crear_proyecto',
        'cli.guardar_version',
        'cli.ver_historial',
        'cli.restaurar_versiones',
        'cli.info_proyecto',
        'cli.funcion_verficar',
        'cli.eliminar_proyecto',
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

# Collect all flet packages
a.datas += collect_all('flet')[0]
a.binaries += collect_all('flet')[1]
a.datas += collect_all('flet_core')[0]
a.binaries += collect_all('flet_core')[1]
a.datas += collect_all('flet_runtime')[0]
a.binaries += collect_all('flet_runtime')[1]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CRONUX-CRX',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../assets/cronux_icon.ico',
)
