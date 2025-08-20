# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

datas = collect_data_files('mediapipe')
binaries = collect_dynamic_libs('mediapipe')
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        "mediapipe.python._framework_bindings",
        "mediapipe.python.solutions.face_mesh",
        "mediapipe.python.solutions.drawing_utils",
        "mediapipe.python.solutions.drawing_styles",
        "mediapipe.python.solutions.face_detection",
        "mediapipe.python.solutions.hands",
        "mediapipe.python.solutions.pose",
    ],
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
    name='main',
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
