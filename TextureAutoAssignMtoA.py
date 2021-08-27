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

FileNameToChannelDictionary = {'baseColor': 'BaseColor', 'metalness': 'Metallic', 'specularRoughness': 'Roughness', 'normalCamera': 'Normal'}
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
  
  if CurrentFile.find(".1001.") > -1:
    isUDIM = True
  
  FirstUnderscoreIndex = currentFile.find("_")
  FirstPeriodIndex = currentFile.find(".")
  TruncatedFileName = currentFile[FirstUnderscoreIndex + 1:FirstPeriodIndex]
  
  for CurrentDictionaryKey in FileNameToChannelDictionary.keys():
    DictionaryValue = FileNameToChannelDictionary[CurrentDictionaryKey]
    SearchTermList = DictionaryValue.split(", ")
    
    for SearchString in SearchTermList:
      if TruncatedFileName.lower() == SearchString.lower():
        CorrespondingAttribute = CurrentDictionaryKey
        
        if RGBOut.list(CorrespondingAttribute) > 0:
          isRGBOut = True
        
  if CorrespondingAttribute == "normalCamera":
    # do normal map generation and connection
  elif CorrespondingAttribute == "height":
    # do displacement map generation and connection
  else:
    # Handle all other files
      if isRGBOut == True:
        currentFileNode = mel.eval('createRenderNodeCB -as2DTexture "" file ""')
        
        if isUDIM == True:
          cmds.setAttr(currentFileNode + ".uvTilingMode", 3)
        
        # Set file name
        # Connect RGB to shader
        
                     

          
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
