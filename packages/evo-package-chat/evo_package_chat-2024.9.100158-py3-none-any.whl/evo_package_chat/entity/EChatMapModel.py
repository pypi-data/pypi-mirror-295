#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_chat.entity.EChatModel import EChatModel
#========================================================================================================================================
"""EChatMapModel

    EChatModelMap _DOC_
    
"""
class EChatMapModel(EObject):

    VERSION:str="b4e710a6aac7738f0ab545b4a989e566c9cc1559b33b20421069a6f5b09318aa"

    def __init__(self):
        super().__init__()
        
        self.apiPackage:str = None
        self.mapEChatModel:EvoMap = EvoMap()
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.apiPackage, stream)
        self._doWriteMap(self.mapEChatModel, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.apiPackage = self._doReadStr(stream)
        self.mapEChatModel = self._doReadMap(EChatModel, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tapiPackage:{self.apiPackage}",
                f"\tmapEChatModel:{self.mapEChatModel}",
                            ]) 
        return strReturn
    