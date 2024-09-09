#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_assistant.entity.EAssistant import EAssistant
#========================================================================================================================================
"""EAssistantMap

    EAssistant _DOC_
    
"""
class EAssistantMap(EObject):

    VERSION:str="6ba6c078d431ad0fb67f4903e9ea8825454016938b8cfc3e270c74d6cb4c3d41"

    def __init__(self):
        super().__init__()
        
        self.mapEAssistant:EvoMap = EvoMap()
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteMap(self.mapEAssistant, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.mapEAssistant = self._doReadMap(EAssistant, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tmapEAssistant:{self.mapEAssistant}",
                            ]) 
        return strReturn
    