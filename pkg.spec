# -*- mode: python -*-
a = Analysis(['bin/pkg'],
             pathex=['/home/prologic/work/pkg'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pkg',
          debug=False,
          strip=True,
          upx=True,
          console=True )
