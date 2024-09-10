#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiFile import EApiFile
from evo_package_chat.entity.EChatParameter import EChatParameter
from evo_framework.core.evo_core_api.entity.EApiText import EApiText
from evo_framework.core.evo_core_api.entity.EApiFile import EApiFile
#========================================================================================================================================
"""EChatInput

    EChatInput _DOC_
    
"""
class EChatInput(EObject):

    VERSION:str="8d120a53fe1a14db5c617c003b9126485eec1bc7064dfd7e92453adf665d6af2"

    def __init__(self):
        super().__init__()
        
        self.apiToken:str = None
        self.modelID:bytes = None
        self.eAssistantID:bytes = None
        self.sessionID:bytes = None
        self.language:str = None
        self.text:str = None
        self.eApiFile:EApiFile = None
        self.mapEChatParameter:EvoMap = EvoMap()
        self.mapEApiText:EvoMap = EvoMap()
        self.mapEApiFile:EvoMap = EvoMap()
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.apiToken, stream)
        self._doWriteBytes(self.modelID, stream)
        self._doWriteBytes(self.eAssistantID, stream)
        self._doWriteBytes(self.sessionID, stream)
        self._doWriteStr(self.language, stream)
        self._doWriteStr(self.text, stream)
        self._doWriteEObject(self.eApiFile, stream)
        self._doWriteMap(self.mapEChatParameter, stream)
        self._doWriteMap(self.mapEApiText, stream)
        self._doWriteMap(self.mapEApiFile, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.apiToken = self._doReadStr(stream)
        self.modelID = self._doReadBytes(stream)
        self.eAssistantID = self._doReadBytes(stream)
        self.sessionID = self._doReadBytes(stream)
        self.language = self._doReadStr(stream)
        self.text = self._doReadStr(stream)
        self.eApiFile = self._doReadEObject(EApiFile, stream)
        self.mapEChatParameter = self._doReadMap(EChatParameter, stream)
        self.mapEApiText = self._doReadMap(EApiText, stream)
        self.mapEApiFile = self._doReadMap(EApiFile, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tapiToken:{self.apiToken}",
                f"\tmodelID length:{len(self.modelID) if self.modelID else 'None'}",
                f"\teAssistantID length:{len(self.eAssistantID) if self.eAssistantID else 'None'}",
                f"\tsessionID length:{len(self.sessionID) if self.sessionID else 'None'}",
                f"\tlanguage:{self.language}",
                f"\ttext:{self.text}",
                f"\teApiFile:{self.eApiFile}",
                f"\tmapEChatParameter:{self.mapEChatParameter}",
                f"\tmapEApiText:{self.mapEApiText}",
                f"\tmapEApiFile:{self.mapEApiFile}",
                            ]) 
        return strReturn
    