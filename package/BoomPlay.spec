# -*- mode: python -*-
from kivy.deps import sdl2, glew

block_cipher = None


a = Analysis(['..\\welcome.py'],
             pathex=['C:\\Users\\gokul\\Desktop\\COMM\\package'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl', 'Tkconstants', 'Tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas += [('boomplay.kv', '../boomplay.kv', 'DATA')]

exe = EXE(pyz,
          Tree('..\\' ,  excludes=['.git','package', 'compile instructions']),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='BoomPlay',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='..\\icons\\icon.ico')
