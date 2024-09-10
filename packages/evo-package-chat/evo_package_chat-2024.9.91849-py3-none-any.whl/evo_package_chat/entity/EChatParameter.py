#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EChatParameter

    EChatSession _DOC_
    
"""
class EChatParameter(EObject):

    VERSION:str="149773142098cd9c2b92bb2c7d1173d60a56682e97af241ffedfa4ea6a7a8daf"

    def __init__(self):
        super().__init__()
        
        self.key:str = None
        self.value:str = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.key, stream)
        self._doWriteStr(self.value, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.key = self._doReadStr(stream)
        self.value = self._doReadStr(stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tkey:{self.key}",
                f"\tvalue:{self.value}",
                            ]) 
        return strReturn
    