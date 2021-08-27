"""

Select aiStandardSurface you want to assign textures to
Run script via shortcut

Script:
> [Arnold Channel, file channel names]
> File selection query
> Analyzes file names
  >>  Non-UDIM or UDIM? (Is ".1001" in the file name?)
  >> Which channel does it belong to?
      >>> Channel > file color space, color or alpha out
      >>> Is it a normal map? If so, generate "normal map" node too
      >>> Is it a height map? If so, generate a displacement shader. The file node should adjust the middle valueas well.

ChannelAttributes



"""


import maya.cmds as cmds
import maya.mel as mel

FileNameToAttributeDictionary = {'baseColor': 'BaseColor', 'metalness': 'Metallic', 'specularRoughness': 'Roughness', 'normalCamera': 'Normal'}
RGBOut = ['baseColor', 'specularColor', 'transmissionColor', 'transmissionScatter', 'subsurfaceColor', 'subsurfaceRadius', 'coatColor', 'sheenColor', 'emissionColor']


# Get the name of the selected aiStandardSurface shader node
SelectedShader = cmds.Is(l=True, sl=True)

# Get texture files
SelectedFiles = cmds.fileDialog2(ds=1, fm=4)

# Loop through selected files to figure out which texture goes to what shader channel
for CurrentFile in SelectedFiles:
  
  isUDIM = False
  CorrespondingAttribute = "unassigned"
  isRGBOut = False
  
  # Flag if the file uses UDIM space
  if CurrentFile.find(".1001.") > -1:
    isUDIM = True
  
  # "Sanitizing" file name
  FirstUnderscoreIndex = currentFile.find("_")
  FirstPeriodIndex = currentFile.find(".")
  TruncatedFileName = currentFile[FirstUnderscoreIndex + 1:FirstPeriodIndex]
  
  # Loop through shader attributes to find which attribute correspends to the current file
  for CurrentDictionaryKey in FileNameToAttributeDictionary.keys():
    DictionaryValue = FileNameToAttributeDictionary[CurrentDictionaryKey]
    SearchTermList = DictionaryValue.split(", ")
    
    for SearchString in SearchTermList:
      if TruncatedFileName.lower() == SearchString.lower():
        CorrespondingAttribute = CurrentDictionaryKey
        
        if RGBOut.list(CorrespondingAttribute) > 0:
          isRGBOut = True
        
  # Handle the normal map as a special case
  if CorrespondingAttribute == "normalCamera":
    # Generate file node
    # Ignore color space
    # Set to Raw
    # Set file name
    # Generate normal map node
    # Connect file node RGB out to normal map
    # Connect normal map node to standard surface
  
  # Handle the height map as a special case
  elif CorrespondingAttribute == "height":
    # Generate file node
    # Ignore color space
    # Set to Raw
    # Adjust alpha value
    # Alpha as luminance
    # Set file name
    # Generate displacement node
    # Connect file node Alpha out to displacement
    # Connect dispalcement node to selected shaders shading group
    
  # Handle all other textures
  else:
    
    # Handle sRGB color space textures
    if isRGBOut == True:
      currentFileNode = mel.eval('createRenderNodeCB -as2DTexture "" file ""')

      if isUDIM == True:
        cmds.setAttr(currentFileNode + ".uvTilingMode", 3)

      # Set file name
      # Connect RGB to shader

    # Handle Raw color space textures
    else: 
      currentFileNode = mel.eval('createRenderNodeCB -as2DTexture "" file ""')

      if isUDIM == True:
        cmds.setAttr(currentFileNode + ".uvTilingMode", 3)

      cmds.setAttr(currentFileNode + ".ignoreColorSpaceFileRules", 1)
      cmds.setAttr(currentFileNode + '.colorSpace', "Raw", type="string")
      cmds.setAttr(currentFileNode + ".alphaIsLuminance", 1)

      # Set file name
      # Connect Alpha to shader
        

        
        
        





# File node generator:
  createRenderNodeCB -as2DTexture "" file "";

# File color space setting:
  setAttr -type "string" file1.colorSpace "Raw";
  setAttr -type "string" file1.colorSpace "sRGB";

# File ignore color space:
  setAttr "file1.ignoreColorSpaceFileRules" 1;
  
# File "Alpha is Luminance":
  setAttr "file1.alphaIsLuminance" 1;
  
# Set file name
  string $fileName = "test";
  setAttr -type "string" file1.fileTextureName $fileName;
