# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# List of .kv file paths and their corresponding target directories
data_files = [
    ("view/admin/adminDashboard/adminDashboard_view.kv", "./"),
    #("view/admin/configuration/config_view.kv", "./"),
    ("view/admin/notifyClient/notify_view.kv", "./"),
    ("view/admin/report/report_view.kv", "./"),
    ("view/admin/storage/storage_view.kv", "./"),
    ("view/admin/userManagement/manage_user_view.kv", "./"),
    ("view/login/login_view.kv", "./"),
    ("view/navigation/admin_nav.kv", "./"),
    ("view/navigation/clerk_nav.kv", "./"),
    ("view/user/add_id/add_id_view.kv", "./"),
    ("view/user/allocate_id/allocate_id_view.kv", "./"),
    ("view/user/contact/contact_view.kv", "./"),
    ("view/user/dashboard/dashboard_view.kv", "./"),
    ("view/user/search_id/search_id_view.kv", "./"),
    ("view/user_profile/user_profile_view.kv", "./"),
    ("view/sync/sync_view.kv", "./"),
    ("view/main_view.kv", "./view"),
#    ("C:\\Users\\HKay\\kivy_venv\\Lib\\site-packages\\escpos\\capabilities.json", "escpos"),
    ("C:\\Users\\HKay\\kivy_venv\\Lib\\site-packages\\escpos\\", "escpos"),
    ("model/database/id_inventory1.db", "./database"),
    ("Assets/Coat_of_arms_of_Malawi.svg", "./Assets"),
    ("favicon.ico", "./")
]

hiddenimports = [
    'kivy', 'kivy.uix.screenmanager', 'kivy.lang', 'kivy.properties',
    'kivy.core.window', 'kivy.core.audio', 'kivy.core.text', 'kivy.core.image', 
    'kivy.graphics', 'kivy.factory', 'kivymd', 'kivymd.app', 'kivymd.uix.button',
    'kivymd.uix.dialog', 'kivymd.uix.label', 'kivymd.uix.textfield', 
    'kivymd.uix.snackbar', 'kivymd.uix.card', 'kivymd.uix.navigationdrawer', 
    'kivymd.uix.list', 'kivymd.uix.toolbar', 'kivymd.uix.gridlayout', 
    'kivymd.uix.stacklayout', 'kivymd.uix.boxlayout', 'kivymd.uix.floatlayout',
    'kivymd.uix.relativelayout', 'kivymd.uix.screen', 'kivymd.uix.scrollview',
    'kivymd.uix.datatables', 'kivymd.uix.menu', 'kivymd.uix.selection', 
    'controller.id_controller', 'controller.dashboard_controller', 'model.user_model',
    'model.some_other_model', 'os', 'sys', 'sqlite3', 'json', 'time', 
    'datetime', 're', 'random', 'requests', 'collections', 'threading', 
    'logging', 'kivymd.uix.navigationrail', 'kivymd.uix.dropdownitem', 'usb.core',
]
hiddenimports += collect_submodules('openpyxl')
hiddenimports += collect_submodules('escpos')
hiddenimports += collect_submodules('numpy')
data_files += collect_data_files('numpy')

# Convert kv_files list into datas format required by PyInstaller
datas = [(Path(src), dst) for src, dst in data_files]

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='IDInventoryManager',
    debug=True,
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
