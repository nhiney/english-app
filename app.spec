# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

# Get the absolute path to the app directory
app_dir = os.path.abspath('app')

a = Analysis(
    ['app/main.py'],
    pathex=[app_dir],  # Add app directory to path
    binaries=[],
    datas=[
        ('app/data', 'app/data'),  # Include data directory
        ('app/assets', 'app/assets')  # Include assets directory
    ],
    hiddenimports=[
        'app.auth',
        'app.home',
        'app.common',
        'app.utils'
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
    name='EnglishApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
) 