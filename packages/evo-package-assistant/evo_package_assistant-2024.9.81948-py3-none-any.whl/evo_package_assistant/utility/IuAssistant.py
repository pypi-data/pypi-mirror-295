#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework import *
from evo_package_assistant.utility.UAssistantApi import UAssistantApi
from evo_package_assistant.entity import *
# ---------------------------------------------------------------------------------------------------------------------------------------
# IuAssistant
# ---------------------------------------------------------------------------------------------------------------------------------------
""" IuAssistant
"""
class IuAssistant(object):
   
    @staticmethod
    def doSet(eAssistant:EAssistant) :
        if eAssistant is None:
            raise Exception("ERROR_eAssistant_NONE")  
        UAssistantApi.getInstance().doSetEAssistant(eAssistant)
        
    @staticmethod
    async def doGet(id:str) :
        if id is None:
            raise Exception("ERROR_id_NONE")
        return await UAssistantApi.getInstance().doGetEAssistant(id)
        
    @staticmethod
    async def doDelEAssistant(id:str) :
        if id is None:
            raise Exception("ERROR_id_NONE")
        await UAssistantApi.getInstance().doDelEAssistant(id)