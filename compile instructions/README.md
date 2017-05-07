# Compile Instructions To Export the project as a windows executable.

### Mode 1: Dependencies visible( Not a single executable).

###### Step 1:
 Install [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/).

###### Step 2:

 Create \<newfolder\> inside the root of the package. 

     cd <newfolder>

###### Step 3:

    python -m PyInstaller --name BoomPlay --icon ..\icons\icon.ico ..\welcome.py

###### Step 4:

 Add this line to the imports in \<newfolder\>/BoomPlay.spec file.

    from kivy.deps import sdl2, glew

###### Step 5:

 Replace the coll initialization line in in \<newfolder\>/BoomPlay.spec with this one.

     coll = COLLECT(exe, Tree('..\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='BoomPlay')

###### Step 6:

    python -m PyInstaller BoomPlay.spec

Reference: [Kivy Website](https://kivy.org/docs/guide/packaging-windows.html)    

### Mode 2: To create a Single Executable

###### Step 1:

 Do Step 1 above
 
 Uncomment the resourcePath in welcome.py at package-root.Add this line to the main function.

     kivy.resources.resource_add_path(resourcePath())

###### Step 2:

    cd package/
    python -m PyInstaller BoomPlay.spec

The exe file is generated in package/dist.    
    


#### Notes:

To prevent force close conflicts, add this line after imports in vlc.py

    ctypes.windll.kernel32.SetDllDirectoryW(None)
