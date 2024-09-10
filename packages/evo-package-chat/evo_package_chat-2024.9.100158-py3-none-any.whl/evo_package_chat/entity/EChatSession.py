#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EChatSession

    EChatSession _DOC_
    
"""
class EChatSession(EObject):

    VERSION:str="44a9de4d353e211011d3454990ba6813f429a8327991129571dd40740b8d70f9"

    def __init__(self):
        super().__init__()
        
        self.name:str = None
        self.sessionID:bytes = None
        self.sessionApi:str = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.name, stream)
        self._doWriteBytes(self.sessionID, stream)
        self._doWriteStr(self.sessionApi, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.name = self._doReadStr(stream)
        self.sessionID = self._doReadBytes(stream)
        self.sessionApi = self._doReadStr(stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tname:{self.name}",
                f"\tsessionID length:{len(self.sessionID) if self.sessionID else 'None'}",
                f"\tsessionApi:{self.sessionApi}",
                            ]) 
        return strReturn
    