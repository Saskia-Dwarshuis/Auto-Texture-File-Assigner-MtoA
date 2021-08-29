## Automatic Texture File Assigner (for Maya and Arnold's aiStandardSurface)

### Reason for existence

Having to assign texture files to aiStandardSurface is not fun. Creating each file node, assigning each file path, and changing the file color space as needed is tedious work that often takes more time than it should. *AutoTextureFileAssignerMtoA.py* is a script designed to mostly automate this process for you.

### How to use the script

1. In the Hypershade editor, select the aiStandardSurface node that you want to connect texture files to.
2. Run the script via a hotkey or the script editor.
3. In the file selection dialog that pops up, select the files you wish to connect to the shader.
    1. The file names should be formatted as follows: *(FilePrefix_)ShaderChannel(.UDIM).FileType*
    2. If you are working with UDIMs, select the first file in the series.
4. Press the file selection dialog's "Open" button when done selecting files.
5. The script will do its magic! File nodes will be generated, their settings updated to fit how the file should be used by the shader, then connected to the selected shader.

### How the script works

The name of each user-selected file is parsed for what shader channel it is supposed to connect to. Once the script knows that, it can generate file nodes with the appropriate color space, uv tiling settings, file path, and connect them to the selected aiStandardSurface node for you! For normal maps, an aiNormalMap node will be generated alongside the file node. For height maps, a displacement node will be generated alongside the file node and connected to the selected shader's upstream shading engine node.

You can change what the script looks for in file names for each channel by modifying the dictionary *FileNameToAttributeDictionary* in *AutoTextureFileAssignerMtoA.py*. See the script for additional details.

### Notices

Tested in Maya 2020/Python 2.7.11. Backwards or forwards compatibility with different Maya or Python versions is not guaranteed.

Released under MIT License (see [LICENSE.md](/LICENSE.md) for more details.)
