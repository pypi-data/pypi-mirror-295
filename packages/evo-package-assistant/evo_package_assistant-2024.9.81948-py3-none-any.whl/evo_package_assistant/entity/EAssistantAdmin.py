#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiAdmin import EApiAdmin
from evo_framework.core.evo_core_api.entity.EApiQuery import EApiQuery
#========================================================================================================================================
"""EAssistantAdmin

    EAssistantAdmin _DOC_
    
"""
class EAssistantAdmin(EObject):

    VERSION:str="6f800aa8126240e053a63546b4b0f85a553a25b158b5111545537ddd5a060a8a"

    def __init__(self):
        super().__init__()
        
        self.eApiAdmin:EApiAdmin = None
        self.eApiQuery:EApiQuery = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteEObject(self.eApiAdmin, stream)
        self._doWriteEObject(self.eApiQuery, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.eApiAdmin = self._doReadEObject(EApiAdmin, stream)
        self.eApiQuery = self._doReadEObject(EApiQuery, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\teApiAdmin:{self.eApiAdmin}",
                f"\teApiQuery:{self.eApiQuery}",
                            ]) 
        return strReturn
    