#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EAssistantAction

    EAssistantAction _DOC_
    
"""
class EAssistantAction(EObject):

    VERSION:str="b14e0938e7d4a71cc8b542bcc93aa2c845007bf8df6df6226cf1077756651b1c"

    def __init__(self):
        super().__init__()
        
        self.message:str = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.message, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.message = self._doReadStr(stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tmessage:{self.message}",
                            ]) 
        return strReturn
    