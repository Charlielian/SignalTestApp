# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['src/main.py'],
             pathex=['.'],
             binaries=[],
             datas=[
                 ('src/ui', 'ui'),
                 ('src/models', 'models'),
                 ('README.md', '.')
             ],
             hiddenimports=[
                 'yaml'
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

executable = EXE(pyz,
                 a.scripts,
                 a.binaries,
                 a.zipfiles,
                 a.datas,
                 [],
                 name='monitor_optimization_tool',
                 debug=False,
                 bootloader_ignore_signals=False,
                 strip=False,
                 upx=True,
                 upx_exclude=[],
                 runtime_tmpdir=None,
                 console=True)