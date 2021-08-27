import maya.cmds as cmds
import maya.mel as mel

# Shader attribute / texture file name dictionary
# To add additional search terms to an attribute, enter as a comma delimited list 
  # Eg. 'normalCamera': 'Normal' >>> 'normalCamera': 'Normal, OpenGLNormal, DirectXNormal'
FileNameToAttributeDictionary = {
  'base': 'BaseWeight', 'baseColor': 'BaseColor', 'diffuseRoughness': 'DiffuseRoughness', 'metalness': 'Metallic', 
  'specular': 'SpecularWeight', 'specularColor': 'SpecularColor', 'specularRoughness': 'Roughness', 
  'transmission': 'TransmissionWeight', 'transmissionColor': 'TransmissionColor', 'transmissionDepth': 'TransmissionDepth', 
  'transmissionScatter': 'TransmissionScatter', 'transmissionExtraRoughness': 'TransmissionExtraRoughness',
  'subsurface': 'SubsurfaceWeight', 'subsurfaceColor': 'SubsurfaceColor', 'subsurfaceRadius': 'SubsurfaceRadius',
  'coat': 'CoatWeight', 'coatColor': 'CoatColor', 'coatRoughness': 'CoatRoughness', 
  'sheen': 'SheenWeight', 'sheenColor': 'SheenColor', 'sheenRoughness': 'SheenRoughness',
  'emission': 'EmissionWeight', 'emissionColor': 'EmissionColor', 
  'opacity': 'Opacity', 'normalCamera': 'Normal', 'height': 'Height'
}

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
    cmds.connectAttr(currentFileNode + '.outColor', NormalMapUtility + '.input', f=True)
    cmds.connectAttr(NormalMapUtility + '.outValue', SelectedShader + '.normalCamera', f=True) 
  
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
    cmds.connectAttr(currentFileNode + '.outAlpha', DisplacementShader + '.displacement', f=True)
    ShadingEngineShader = cmds.listConnections(SelectedShader, t="shadingEngine", s=False)
    cmds.connectAttr(DisplacementShader + '.displacement', ShadingEngineShader[0] + '.displacementShader', f=True)
    

  # Handle all other textures
  else:
    
    # Handle sRGB color space textures
    if isRGBOut == True:
      currentFileNode = mel.eval('createRenderNodeCB -as2DTexture "" file ""')

      if isUDIM == True:
        cmds.setAttr(currentFileNode + ".uvTilingMode", 3)
      
      cmds.setAttr(currentFileNode + '.fileTextureName', CurrentFile, type="string")
      cmds.connectAttr(currentFileNode + '.outColor', SelectedShader + '.' + CorrespondingAttribute, f=True)

    # Handle Raw color space textures
    else: 
      currentFileNode = mel.eval('createRenderNodeCB -as2DTexture "" file ""')

      if isUDIM == True:
        cmds.setAttr(currentFileNode + ".uvTilingMode", 3)

      cmds.setAttr(currentFileNode + ".ignoreColorSpaceFileRules", 1)
      cmds.setAttr(currentFileNode + '.colorSpace', "Raw", type="string")
      cmds.setAttr(currentFileNode + ".alphaIsLuminance", 1)
      cmds.setAttr(currentFileNode + '.fileTextureName', CurrentFile, type="string")     
      cmds.connectAttr(currentFileNode + '.outAlpha', SelectedShader + '.' + CorrespondingAttribute, f=True)
