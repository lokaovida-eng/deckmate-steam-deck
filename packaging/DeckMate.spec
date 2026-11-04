# PyInstaller build definition for the DeckMate AppImage.
from PyInstaller.utils.hooks import collect_all
from pathlib import Path

root = Path(SPECPATH).parent
datas, binaries, hiddenimports = collect_all("copilot")

a = Analysis(
    [str(root / "assistente.py")],
    pathex=[str(root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "pytest"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    name="DeckMate",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    exclude_binaries=True,
    disable_windowed_traceback=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="DeckMate",
)
