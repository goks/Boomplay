###### Step1:
 Install [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/).

###### Step2:

 Create newfolder inside the root of the package. 

     cd <newfolder>

###### Step3:

    python -m PyInstaller --name BoomPlay --icon ..\icons\icon.ico ..\welcome.py

######Step4:

 Add this line to the imports in <newfolder>/BoomPlay.spec file

    from kivy.deps import sdl2, glew

###### Step5:

 Replace the coll initialization line with this one

     coll = COLLECT(exe, Tree('..\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='BoomPlay')

###### Step6:

    python -m PyInstaller BoomPlay.spec

[Details from Kivy Website](https://kivy.org/docs/guide/packaging-windows.html)    

######Notes:

add this line after imports in vlc.py

    ctypes.windll.kernel32.SetDllDirectoryW(None)
