## Automatic Texture File Assigner (for Maya and Arnold's aiStandardSurface)

### The Why

Having to assign texture files to aiStandardSurface is not fun. Creating each file node, assigning each file path, and changing the file color space as needed is tedious work that often takes more time than it should. *AutoTextureFileAssignerMtoA.py* is a script designed to mostly automate this process for you. 

### The What
*AutoTextureFileAssignerMtoA.py* is built for Maya for use with Arnold's aiStandardSurface shader. It works as such:

1. In the Hypershade, select the aiStandardSurface node that you want to connect texture files to. 
2. Run the script via hotkey or script editor.
3. In the file selection dialog that pops up, select the files you wish to connect to the shader.
    1. The file names should be forrmated as follows: *(FilePrefix_)ShaderChannel(.UDIM).FileType*
    2. If you are working with UDIMs, select only one file in the series.  
4. Press the file selection dialog's "Open" button when done selecting files.
5. The script will do its magic! 

### The How

[Assign as a hotkey]



### Notices

Tested in Maya 2020/Python 2.7.11. Backwards or forwards compatibility with different Maya or Python versions is not guaranteed. 

Released under MIT License (see [LICENSE.md](/LICENSE.md) for more details.)
