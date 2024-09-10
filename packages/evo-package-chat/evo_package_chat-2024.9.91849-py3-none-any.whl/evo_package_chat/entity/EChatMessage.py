#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiText import EApiText
from evo_framework.core.evo_core_api.entity.EApiText import EApiText
from evo_framework.core.evo_core_api.entity.EApiFile import EApiFile
#========================================================================================================================================
"""EChatMessage

    EChatMessage _DOC_
    
"""
class EChatMessage(EObject):

    VERSION:str="281c6a7a6577255726af024025afe1fe4f19ec97a70310353e86d8b5a1c1f9be"

    def __init__(self):
        super().__init__()
        
        self.model:str = None
        self.eAssistantID:bytes = None
        self.sessionID:bytes = None
        self.eApiText:EApiText = None
        self.isError:bool = None
        self.error:str = None
        self.mapEApiText:EvoMap = EvoMap()
        self.mapEApiFile:EvoMap = EvoMap()
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.model, stream)
        self._doWriteBytes(self.eAssistantID, stream)
        self._doWriteBytes(self.sessionID, stream)
        self._doWriteEObject(self.eApiText, stream)
        self._doWriteBool(self.isError, stream)
        self._doWriteStr(self.error, stream)
        self._doWriteMap(self.mapEApiText, stream)
        self._doWriteMap(self.mapEApiFile, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.model = self._doReadStr(stream)
        self.eAssistantID = self._doReadBytes(stream)
        self.sessionID = self._doReadBytes(stream)
        self.eApiText = self._doReadEObject(EApiText, stream)
        self.isError = self._doReadBool(stream)
        self.error = self._doReadStr(stream)
        self.mapEApiText = self._doReadMap(EApiText, stream)
        self.mapEApiFile = self._doReadMap(EApiFile, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tmodel:{self.model}",
                f"\teAssistantID length:{len(self.eAssistantID) if self.eAssistantID else 'None'}",
                f"\tsessionID length:{len(self.sessionID) if self.sessionID else 'None'}",
                f"\teApiText:{self.eApiText}",
                f"\tisError:{self.isError}",
                f"\terror:{self.error}",
                f"\tmapEApiText:{self.mapEApiText}",
                f"\tmapEApiFile:{self.mapEApiFile}",
                            ]) 
        return strReturn
    