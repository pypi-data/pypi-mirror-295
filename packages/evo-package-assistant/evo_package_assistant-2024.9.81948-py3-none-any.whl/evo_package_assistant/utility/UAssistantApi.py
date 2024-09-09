#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_assistant.entity import *
from evo_framework.core.evo_core_api.entity.EApiQuery import EApiQuery

#<
import importlib.util
from pathlib import Path
from evo_package_assistant.control.CAssistantCallback import CAssistantCallback

#>
# ---------------------------------------------------------------------------------------------------------------------------------------
# UAssistantApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""UAssistantApi
"""
class UAssistantApi():
    __instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):   
        if UAssistantApi.__instance != None:
            raise Exception("ERROR:SINGLETON")
        else:
            super().__init__()
            UAssistantApi.__instance = self
            self.pathAssistant:str|Any = None
            self.eAssistantMap:EAssistantMap = EAssistantMap()
            
# ---------------------------------------------------------------------------------------------------------------------------------------
    """getInstance Singleton

    Raises:
        Exception:  api exception

    Returns:
        _type_: UAssistantApi instance
    """
    @staticmethod
    def getInstance():
        if UAssistantApi.__instance is None:
            uObject = UAssistantApi()  
            #uObject.doInit()  
        return UAssistantApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
    """doInit

    Raises:
        Exception: api exception

    Returns:

    """   
    def doInit(self, isSkipLoad=False):
        try:
#<
            self.eAssistantMap.doGenerateID()
            pathAssistantTmp = CSetting.getInstance().doGet("CYBORGAI_PATH_ASSETS_ASSISTANT")
        
            if IuText.StringEmpty(pathAssistantTmp):
                #IuLog.doError(__name__, f"ERROR_REQUIRED_ENV|CYBORGAI_PATH_ASSETS_ASSISTANT")
                pathAssistantTmp= "~/cyborgai/peer/peer-python/assistant"
                pathAssistantTmp = os.path.expanduser(pathAssistantTmp)
                IuLog.doInfo(__name__, f"CYBORGAI_PATH_ASSETS_ASSISTANT:{pathAssistantTmp}")
              
            self.pathAssistant = pathAssistantTmp  
            IuLog.doVerbose(__name__, f"pathAssistant:{self.pathAssistant}")

            if not isSkipLoad:
                self.__doLoadDirEAssistant()         
#>   
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnSet(self, eAction:EAction) -> EAction:
        """doOnSet utility callback
            input: EAssistantAdmin
            output: EAssistant

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eAssistantAdmin:EAssistantAdmin = eAction.doGetInput(EAssistantAdmin)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eAssistantAdmin is None:
                raise Exception("ERROR_REQUIRED|eAssistantAdmin|")

#<        
            #Add other check
            
            if eAssistantAdmin.eApiAdmin is None:
                raise Exception("ERROR_REQUIRED|eAssistantAdmin.eApiAdmin")
            
            
            
            
            #TODO:check admin otp
            
            
   
            eAssistant = EAssistant()
            eAssistant.doGenerateID()
          
            eAction.enumApiAction = EnumApiAction.COMPLETE
            IuLog.doVerbose(__name__, f"eAssistant:{eAssistant}")
            
            eAction.doSetOutput(eAssistant)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnGet(self, eAction:EAction) -> EAction:
        """doOnGet utility callback
            input: EApiQuery
            output: EAssistant

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eApiQuery:EApiQuery = eAction.doGetInput(EApiQuery)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eApiQuery is None:
                raise Exception("ERROR_REQUIRED|eApiQuery|")

#<        
            #Add other check
            
            if eApiQuery.eObjectID is None:
                raise Exception("ERROR_REQUIRED|eApiQuery.eObjectID")
            
            eAssistant = self.eAssistantMap.mapEAssistant.doGet(eApiQuery.eObjectID)
        
            if eAssistant is None:
                raise Exception("ERROR_REQUIRED|eAssistant")
        
        
            eAction.enumApiAction = EnumApiAction.COMPLETE
            eAction.doSetOutput(eAssistant)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnDel(self, eAction:EAction) -> EAction:
        """doOnDel utility callback
            input: EAssistantAdmin
            output: EAssistant

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eAssistantAdmin:EAssistantAdmin = eAction.doGetInput(EAssistantAdmin)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eAssistantAdmin is None:
                raise Exception("ERROR_REQUIRED|eAssistantAdmin|")

#<        
            #Add other check
            '''
            if eAssistantAdmin. is None:
                raise Exception("ERROR_REQUIRED|eAssistantAdmin.|")
            '''
   
            eAssistant = EAssistant()
            eAssistant.doGenerateID()
            eAssistant.doGenerateTime()

            eAction.enumApiAction = EnumApiAction.COMPLETE
            IuLog.doVerbose(__name__, f"eAssistant:{eAssistant}")
            eAction.doSetOutput(eAssistant)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnQuery(self, eAction:EAction) -> EAction:
        """doOnQuery utility callback
            input: EApiQuery
            output: EAssistantMap

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eApiQuery:EApiQuery = eAction.doGetInput(EApiQuery)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eApiQuery is None:
                raise Exception("ERROR_REQUIRED|eApiQuery|")

#<        
            #Add other check
            '''
            if eApiQuery. is None:
                raise Exception("ERROR_REQUIRED|eApiQuery.|")
            '''
            eAssistantMap = self.eAssistantMap

            eAction.enumApiAction = EnumApiAction.COMPLETE
            IuLog.doVerbose(__name__, f"eAssistantMap:{eAssistantMap}")
            eAction.doSetOutput(eAssistantMap)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------

#<
    async def doGetEAssistant(self, id:bytes) -> EAssistant:
        try:
            #id = bytes.fromhex(idIn)
            idStr = IuKey.toString(id).lower().replace(" ","_")
            if id in self.eAssistantMap.mapEAssistant.keys():
                return self.eAssistantMap.mapEAssistant.doGet(id)
            else:
                pathAssistant = f"{self.pathAssistant}/assistant_{idStr}.yaml"
                self.__doLoadEAssistant(pathAssistant)
                
                IuLog.doVerbose(__name__, self.eAssistantMap)
                
                if id in self.eAssistantMap.mapEAssistant.keys():
                    return self.eAssistantMap.mapEAssistant.doGet(id)
                
                IuLog.doError(__name__,f"ERROR_NOT_FOUND_ASSISTANT|{pathAssistant}")
                
                raise Exception(f"ERROR_NOT_FONUD_ASSISTANT|{idStr}")
            
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------

    def __doLoadDirEAssistant(self):
        try:
            if self.pathAssistant is None:
                IuLog.doError(__name__, f"ERROR_REQUIRED_ENV|CYBORGAI_PATH_ASSETS_ASSISTANT")
            else:
                IuLog.doVerbose(__name__, f"self.pathAssistant {self.pathAssistant}")
                
                directory = Path(self.pathAssistant)
                
                arrayFileAssistant = [str(file) for file in directory.rglob('assistant_*.yaml')]
                
                if len(arrayFileAssistant) == 0:
                    IuLog.doWarning(__name__, f"WARNING:pathAssistant empty download assistant in {self.pathAssistant}")
                
                IuLog.doVerbose(__name__,f"arrayFileAssistant:\n{arrayFileAssistant}")

                for pathAssistant in arrayFileAssistant:
                    self.__doLoadEAssistant(pathAssistant)
                
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
        
#-------------------------------------------------------------------------------
    def __doLoadEAssistant(self, pathAssistant):
        try:
            IuLog.doVerbose(__name__,f"pathAssistant: {pathAssistant}")
            
            mapAssistantFull = IuYAml.doLoad(pathAssistant)
            
            IuLog.doVerbose(__name__, f"{mapAssistantFull}")
        
            eAssistant = EAssistant()
            
            mapAssistant = mapAssistantFull["assistant"]
            
            name = str(mapAssistant["name"])
            systemMessage = str(mapAssistant["SYSTEM"])
            description = str(mapAssistant["description"])
            logo = str(mapAssistant["logo"])
            
            if "messages" in  mapAssistant: 
                arrayMessage = mapAssistant["messages"]
                for mapMessage in arrayMessage:
                    for messageRole, message in mapMessage.items():
                        role = str(messageRole).upper()
                        
                        enumAssistantRole = EnumAssistantRole.ASSISTANT
                        if role == "USER":
                            enumAssistantRole =  EnumAssistantRole.USER
                            
                        eAssistant.addMessage(enumAssistantRole, str(message))
                
           
            if "action" in  mapAssistantFull:    
                actionStr = ""   
                mapAction = mapAssistantFull["action"]
                for key, value in mapAction.items():
                    eAssistantAction = EAssistantAction()
                    eAssistantAction.doGenerateID(str(key))
                    eAssistantAction.doGenerateTime()
                    eAssistantAction.message = str(value)
                    actionStr = "\n".join([actionStr, f"{key}: {value}"])
                    eAssistant.mapAction.doSet(eAssistantAction)
                systemMessage = systemMessage.format(action_list = actionStr )
             
            idStr = name.replace(" ", "_").lower()               
            eAssistant.doGenerateID(f"{idStr}", isHash=False)
            eAssistant.name = f"{name}"
            eAssistant.systemMessage = systemMessage
            eAssistant.logo = logo
            eAssistant.description = description
            
            eAssistant.callback = CAssistantCallback(mapAssistantFull)
            
            if eAssistant.callback is None:
                raise Exception("ERROR_NOT_VALID|eAssistant.callback")
            
            self.eAssistantMap.mapEAssistant.doSet(eAssistant)
            
            IuLog.doVerbose(__name__, eAssistant)
            
            return eAssistant
                     
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
