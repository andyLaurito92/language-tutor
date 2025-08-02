# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for AI Language Tutor macOS application.
This file defines how to bundle the Python application into a macOS .app bundle.
"""

from pathlib import Path
import os

# Get the current directory
current_dir = Path.cwd()

# Define the main script
main_script = str(current_dir / "launcher.py")

# Define data files to include
data_files = [
    (str(current_dir / "app.py"), "."),
    (str(current_dir / "cli_tutor.py"), "."),
    (str(current_dir / "src"), "src"),
    (str(current_dir / "data"), "data"),
    (str(current_dir / ".env.example"), "."),
    (str(current_dir / "requirements.txt"), "."),
    (str(current_dir / "requirements_no_audio.txt"), "."),
]

# Hidden imports needed by the application
hidden_imports = [
    'streamlit',
    'streamlit.web.cli',
    'streamlit.runtime.scriptrunner.script_runner',
    'streamlit.runtime.state',
    'streamlit.runtime.caching',
    'streamlit.components.v1',
    'altair',
    'plotly',
    'pandas',
    'numpy',
    'requests',
    'python_dotenv',
    'src.utils.config',
    'src.utils.database',
    'src.tutor.ai_tutor',
    'src.tutor.speech',
    'src.tutor.lessons',
]

# Additional packages that might be needed
packages = [
    'streamlit',
    'altair',
    'plotly.graph_objs',
    'plotly.express',
    'plotly.io',
]

a = Analysis(
    [main_script],
    pathex=[str(current_dir)],
    binaries=[],
    datas=data_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5',
        'PyQt6', 
        'PySide2',
        'PySide6',
        'tkinter',
        'matplotlib.backends._backend_tk',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ai-language-tutor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to False for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an .icns file here later
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ai-language-tutor',
)

app = BUNDLE(
    coll,
    name='AI Language Tutor.app',
    icon=None,  # You can add an .icns file here later
    bundle_identifier='com.andylaurito92.language-tutor',
    version='1.0.0',
    info_plist={
        'CFBundleName': 'AI Language Tutor',
        'CFBundleDisplayName': 'AI Language Tutor',
        'CFBundleIdentifier': 'com.andylaurito92.language-tutor',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleInfoDictionaryVersion': '6.0',
        'CFBundleExecutable': 'ai-language-tutor',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': '????',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
        'LSMinimumSystemVersion': '10.13.0',
        'NSHumanReadableCopyright': 'Copyright © 2024 Andy Laurito. All rights reserved.',
        'CFBundleDocumentTypes': [],
        'UTExportedTypeDeclarations': [],
        'NSPrincipalClass': 'NSApplication',
        'NSMainNibFile': 'MainMenu',
        'LSUIElement': False,  # Set to True to hide from Dock
    },
)