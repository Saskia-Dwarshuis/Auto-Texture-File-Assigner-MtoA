import maya.cmds as cmds
import maya.mel as mel

# Shader attribute / texture file name dictionary
FileNameToAttributeDictionary = {'baseColor': 'BaseColor', 'metalness': 'Metallic', 'specularRoughness': 'Roughness', 'normalCamera': 'Normal', 'height': 'Height'}

# Shader attributes that require RGB color
RGBOut = ['baseColor', 'specularColor', 'transmissionColor', 'transmissionScatter', 'subsurfaceColor', 'subsurfaceRadius', 'coatColor', 'sheenColor', 'emissionColor']

# Get the name of the selected aiStandardSurface shader node
SelectedShader = cmds.ls(l=True, type="aiStandardSurface", sl=True)
SelectedShader = SelectedShader[0]

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
  FirstUnderscoreIndex = CurrentFile.find("_")
  FirstPeriodIndex = CurrentFile.find(".")
  TruncatedFileName = CurrentFile[FirstUnderscoreIndex + 1:FirstPeriodIndex]
  
  # Loop through shader attributes to find which attribute correspends to the current file
  for CurrentDictionaryKey in FileNameToAttributeDictionary.keys():
    DictionaryValue = FileNameToAttributeDictionary[CurrentDictionaryKey]
    SearchTermList = DictionaryValue.split(", ")
    
    for SearchString in SearchTermList:
      if TruncatedFileName.lower() == SearchString.lower():
        CorrespondingAttribute = CurrentDictionaryKey
        
        if CorrespondingAttribute in RGBOut:
          isRGBOut = True
        
  # Handle the normal map as a special case
  if CorrespondingAttribute == "normalCamera":    
    currentFileNode = mel.eval('createRenderNodeCB -as2DTexture "" file ""')
      
    if isUDIM == True:
      cmds.setAttr(currentFileNode + ".uvTilingMode", 3)
      
    cmds.setAttr(currentFileNode + ".ignoreColorSpaceFileRules", 1)
    cmds.setAttr(currentFileNode + '.colorSpace', "Raw", type="string")
    cmds.setAttr(currentFileNode + '.fileTextureName', CurrentFile, type="string")
    NormalMapUtility = cmds.shadingNode('aiNormalMap', asUtility=True)
    cmds.connectAttr(currentFileNode + '.outColor', NormalMapUtility + '.input')
    cmds.connectAttr(NormalMapUtility + '.outValue', SelectedShader + '.normalCamera') 
  
  # Handle the height map as a special case
  elif CorrespondingAttribute == "height":
    currentFileNode = mel.eval('createRenderNodeCB -as2DTexture "" file ""')
    
    if isUDIM == True:
        cmds.setAttr(currentFileNode + ".uvTilingMode", 3)
    
    cmds.setAttr(currentFileNode + ".ignoreColorSpaceFileRules", 1)
    cmds.setAttr(currentFileNode + '.colorSpace', "Raw", type="string")
    cmds.setAttr(currentFileNode + ".alphaOffset", -0.5)
    cmds.setAttr(currentFileNode + ".alphaIsLuminance", 1)
    cmds.setAttr(currentFileNode + '.fileTextureName', CurrentFile, type="string")
    DisplacementShader = mel.eval('createRenderNodeCB -asShader "displacementShader" displacementShader ""')
    cmds.connectAttr(f=True, currentFileNode + ".outAlpha", DisplacementShader[0] + ".displacement")
    ShadingEngineShader = cmds.listConnections(SelectedShader, s=False, t="shadingEngine")
    cmds.connectAttr(f=True, DisplacementShader[0] + ".displacement", ShadingEngineShader[0] + ".displacementShader")
    
  # Handle all other textures
  else:
    
    # Handle sRGB color space textures
    if isRGBOut == True:
      currentFileNode = mel.eval('createRenderNodeCB -as2DTexture "" file ""')

      if isUDIM == True:
        cmds.setAttr(currentFileNode + ".uvTilingMode", 3)
      
      cmds.setAttr(currentFileNode + '.fileTextureName', CurrentFile, type="string")
      cmds.connectAttr(f=True, currentFileNode + ".outColor", SelectedShader + "." + CorrespondingAttribute)

    # Handle Raw color space textures
    else: 
      currentFileNode = mel.eval('createRenderNodeCB -as2DTexture "" file ""')

      if isUDIM == True:
        cmds.setAttr(currentFileNode + ".uvTilingMode", 3)

      cmds.setAttr(currentFileNode + ".ignoreColorSpaceFileRules", 1)
      cmds.setAttr(currentFileNode + '.colorSpace', "Raw", type="string")
      cmds.setAttr(currentFileNode + ".alphaIsLuminance", 1)
      cmds.setAttr(currentFileNode + '.fileTextureName', CurrentFile, type="string")     
      cmds.connectAttr(f=True, currentFileNode + ".outAlpha", SelectedShader + "." + CorrespondingAttribute)
