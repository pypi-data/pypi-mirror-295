#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EAssistantToolParam

    EAssistantToolParam _DOC_
    
"""
class EAssistantToolParam(EObject):

    VERSION:str="c897fff31b14bb5a1e721cbeba2291204f3b6c74079a14714a9b56ff1aa2c0f9"

    def __init__(self):
        super().__init__()
        
        self.type:str = None
        self.isRequired:bool = True
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.type, stream)
        self._doWriteBool(self.isRequired, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.type = self._doReadStr(stream)
        self.isRequired = self._doReadBool(stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\ttype:{self.type}",
                f"\tisRequired:{self.isRequired}",
                            ]) 
        return strReturn
    