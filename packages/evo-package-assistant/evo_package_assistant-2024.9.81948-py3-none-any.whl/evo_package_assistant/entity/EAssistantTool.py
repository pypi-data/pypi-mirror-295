#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_assistant.entity.EAssistantToolParam import EAssistantToolParam
#========================================================================================================================================
"""EAssistantTool

    EAssistantTool _DOC_
    
"""
class EAssistantTool(EObject):

    VERSION:str="028f6050ba8d7d4336167f4be16ceeeb2b1f673358494dc95ad26c2855f5cde6"

    def __init__(self):
        super().__init__()
        
        self.description:str = None
        self.mapEAssistantToolParam:EvoMap = EvoMap()
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.description, stream)
        self._doWriteMap(self.mapEAssistantToolParam, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.description = self._doReadStr(stream)
        self.mapEAssistantToolParam = self._doReadMap(EAssistantToolParam, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tdescription:{self.description}",
                f"\tmapEAssistantToolParam:{self.mapEAssistantToolParam}",
                            ]) 
        return strReturn
    