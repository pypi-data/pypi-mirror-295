#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_assistant.entity.EAssistantMessage import EAssistantMessage
from evo_package_assistant.entity.EAssistantTool import EAssistantTool
from evo_package_assistant.entity.EAssistantAction import EAssistantAction
#<
from evo_framework.core.evo_core_crypto.utility.IuCryptHash import IuCryptHash
from evo_package_assistant.entity.EnumAssistantRole import EnumAssistantRole
from evo_framework.core.evo_core_api.entity import *
#>
#========================================================================================================================================
"""EAssistant

    EAssistant _DOC_
    
"""
class EAssistant(EObject):

    VERSION:str="0b23cf5aa5bcbf26491ef830f8e57c48d1e29a115ec668448d5559d94bc19c67"

    def __init__(self):
        super().__init__()
        
        self.name:str = None
        self.description:str = None
        self.systemMessage:str = None
        self.logo:str = None
        self.mapEAssistantMessage:EvoMap = EvoMap()
        self.mapEAssistantTool:EvoMap = EvoMap()
        self.mapAction:EvoMap = EvoMap()
#<
        #NOT SERIALIZED
        self.callback = None
#> 
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.name, stream)
        self._doWriteStr(self.description, stream)
        self._doWriteStr(self.systemMessage, stream)
        self._doWriteStr(self.logo, stream)
        self._doWriteMap(self.mapEAssistantMessage, stream)
        self._doWriteMap(self.mapEAssistantTool, stream)
        self._doWriteMap(self.mapAction, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.name = self._doReadStr(stream)
        self.description = self._doReadStr(stream)
        self.systemMessage = self._doReadStr(stream)
        self.logo = self._doReadStr(stream)
        self.mapEAssistantMessage = self._doReadMap(EAssistantMessage, stream)
        self.mapEAssistantTool = self._doReadMap(EAssistantTool, stream)
        self.mapAction = self._doReadMap(EAssistantAction, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tname:{self.name}",
                f"\tdescription:{self.description}",
                f"\tsystemMessage:{self.systemMessage}",
                f"\tlogo:{self.logo}",
                f"\tmapEAssistantMessage:{self.mapEAssistantMessage}",
                f"\tmapEAssistantTool:{self.mapEAssistantTool}",
                f"\tmapAction:{self.mapAction}",
                            ]) 
        return strReturn
    
#<
     #WRAPPPER
    def addMessage(self, enumAssistantRole:EnumAssistantRole, message:str, eApiFile:EApiFile = None):
        if enumAssistantRole is None:
            raise Exception("ERROR_REQUIRED|enumAssistantRole|")
        
        if message is None:
            raise Exception("ERROR_REQUIRED|message|")
        
        eAssistantMessage = EAssistantMessage()
        eAssistantMessage.doGenerateID(f"{(len(self.mapEAssistantMessage.keys()))}")
        eAssistantMessage.enumAssistantRole = enumAssistantRole
        eAssistantMessage.message = message
        self.mapEAssistantMessage.doSet(eAssistantMessage)
        
        #if eAssistantMessage.enumAssistantRole == EnumAssistantRole.SYSTEM:
        #    self.systemID = eAssistantMessage.id
#>  