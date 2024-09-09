#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_assistant.entity.EnumAssistantRole import EnumAssistantRole
from evo_framework.core.evo_core_api.entity.EApiFile import EApiFile
#========================================================================================================================================
"""EAssistantMessage

    EAssistantChat _DOC_
    
"""
class EAssistantMessage(EObject):

    VERSION:str="caf2e977bb9058e42e04c79c46c1fc13cdf9283b08860676a64728542d6ac335"

    def __init__(self):
        super().__init__()
        
        self.enumAssistantRole:EnumAssistantRole = EnumAssistantRole.USER
        self.message:str = None
        self.eApiFile:EApiFile = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteInt(self.enumAssistantRole.value, stream)
        self._doWriteStr(self.message, stream)
        self._doWriteEObject(self.eApiFile, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.enumAssistantRole = EnumAssistantRole(self._doReadInt(stream))
        self.message = self._doReadStr(stream)
        self.eApiFile = self._doReadEObject(EApiFile, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tenumAssistantRole:{self.enumAssistantRole}",
                f"\tmessage:{self.message}",
                f"\teApiFile:{self.eApiFile}",
                            ]) 
        return strReturn
    