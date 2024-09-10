#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EChatModel

    EChatModel _DOC_
    
"""
class EChatModel(EObject):

    VERSION:str="e407a5d1fb8e52ce9cd9c695a34fd4d77aefb3fc0a4fe2e0f1628691fd166d2c"

    def __init__(self):
        super().__init__()
        
        self.name:str = None
        self.created:int = None
        self.apiPackage:str = None
        self.typeInput:int = None
#<
        self.callback = None
#> 
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.name, stream)
        self._doWriteInt(self.created, stream)
        self._doWriteStr(self.apiPackage, stream)
        self._doWriteInt(self.typeInput, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.name = self._doReadStr(stream)
        self.created = self._doReadInt(stream)
        self.apiPackage = self._doReadStr(stream)
        self.typeInput = self._doReadInt(stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tname:{self.name}",
                f"\tcreated:{self.created}",
                f"\tapiPackage:{self.apiPackage}",
                f"\ttypeInput:{self.typeInput}",
                            ]) 
        return strReturn
    