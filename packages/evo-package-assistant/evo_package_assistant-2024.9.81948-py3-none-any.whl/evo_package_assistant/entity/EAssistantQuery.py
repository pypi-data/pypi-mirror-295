#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EAssistantQuery

    EAssistant _DOC_
    
"""
class EAssistantQuery(EObject):

    VERSION:str="ea156bed21c86c8a99ba7dc3df9f23550f70389422ffdc819bf7e1da548cad0f"

    def __init__(self):
        super().__init__()
        
        self.query:str = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.query, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.query = self._doReadStr(stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tquery:{self.query}",
                            ]) 
        return strReturn
    