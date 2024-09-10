#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_chat.entity.EChatMessage import EChatMessage
#========================================================================================================================================
"""EChatMapMessage

    EChatMapMessage _DOC_
    
"""
class EChatMapMessage(EObject):

    VERSION:str="91204d83e68338881fcc5a72afb5cf031f9b66afb616c84f86e004b442bdb298"

    def __init__(self):
        super().__init__()
        
        self.sessionID:bytes = None
        self.mapEChatMessage:EvoMap = EvoMap()
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteBytes(self.sessionID, stream)
        self._doWriteMap(self.mapEChatMessage, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.sessionID = self._doReadBytes(stream)
        self.mapEChatMessage = self._doReadMap(EChatMessage, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tsessionID length:{len(self.sessionID) if self.sessionID else 'None'}",
                f"\tmapEChatMessage:{self.mapEChatMessage}",
                            ]) 
        return strReturn
    