#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_chat.entity.EChatSession import EChatSession
#========================================================================================================================================
"""EChatMapSession

    EChatMapSession _DOC_
    
"""
class EChatMapSession(EObject):

    VERSION:str="5f9c6b11d520fbb5a84116f98fd9db99ecd3e172eae02367b494094c3895f03c"

    def __init__(self):
        super().__init__()
        
        self.mapEChatSession:EvoMap = EvoMap()
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteMap(self.mapEChatSession, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.mapEChatSession = self._doReadMap(EChatSession, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tmapEChatSession:{self.mapEChatSession}",
                            ]) 
        return strReturn
    