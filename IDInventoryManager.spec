# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

# Specify the path to your .kv file
clerk_nav_path = Path("view/navigation/clerk_nav.kv")
admin_nav_path = Path("view/navigation/admin_nav.kv")



a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[(clerk_nav_path, 'view/navigation'), (admin_nav_path, 'view/navigation')],  # Include the .kv file
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='IDInventoryManager',
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
)
