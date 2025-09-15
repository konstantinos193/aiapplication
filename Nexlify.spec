# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('config', 'config')],
    hiddenimports=['PyQt6.QtCore', 'PyQt6.QtWidgets', 'PyQt6.QtGui', 'OpenGL', 'numpy', 'PIL', 'yaml', 'pydantic'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'matplotlib', 'scipy', 'pytest', 'click', 'rich', 'tqdm', 'auto-py-to-exe', 'Eel', 'bottle', 'gevent', 'lxml', 'jinja2', 'dateutil', 'certifi', 'charset-normalizer', 'idna', 'urllib3', 'requests', 'setuptools', 'wheel', 'pkg_resources', 'platformdirs', 'pycparser', 'cffi', 'greenlet', 'zope.event', 'zope.interface', 'pygments', 'markdown-it-py', 'mdurl', 'iniconfig', 'pluggy', 'packaging', 'pyparsing', 'importlib_resources', 'importlib_metadata', 'zipp', 'jaraco.functools', 'jaraco.text', 'jaraco.context', 'backports.tarfile', 'backports', 'typing_extensions', 'typing_inspection', 'annotated_types', 'pydantic_core', 'colorama', 'six', 'zoneinfo', 'OpenGL_accelerate'],
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
    name='Nexlify',
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
    icon=['assets\\nexlify_icon_simple.ico'],
)
