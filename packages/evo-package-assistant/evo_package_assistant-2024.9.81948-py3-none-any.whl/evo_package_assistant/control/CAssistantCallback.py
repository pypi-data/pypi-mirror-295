#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
import copy
import textwrap
import re
# ---------------------------------------------------------------------------------------------------------------------------------------
# CAssistantCallbackStream
# ---------------------------------------------------------------------------------------------------------------------------------------
"""CAssistantCallbackStream
"""
class CAssistantCallback:
    def __init__(self, config):
        self.config = config
        self.languageAssistant = config['callback'].get('language', 'python')
        self.arraRequirement = config['callback'].get('requirement', [])
        self.header = ""
        self.eApiText:EApiText = EApiText()
        self.isParseHeader:bool = True
        self.header:str = ""
        self.prefixID:str = ""
        self.messageFull:str = ""
        self.count:int = 0
        self.messageHeader:str = None
        self.headerPattern = r'\[.*?\]'
        self.isRemoveHeader:bool = True
        self.chunkHeader:int = -1
        self.totenTot:int=0
        self.mapCallback = {}
        self.headerSize:int = 0
        self.action:str = ""
        self.language:str = ""
        
# ---------------------------------------------------------------------------------------------------------------------------------------  
    def clone(self):
        return copy.deepcopy(self)
    
# ---------------------------------------------------------------------------------------------------------------------------------------  
    """isHeaderComplete
    
    """
    async def isHeaderComplete(self, message) ->bool:
        if not self.isParseHeader:
                self.header=""
                return True
        self.messageFull = "".join([self.messageFull, message])
        if IuText.StringEmpty(self.header):
            match = re.search(self.headerPattern, self.messageFull)  
             
            if match:
                headerFull = match.group()
                self.headerSize = len(headerFull)
                self.header=headerFull.replace("[","").replace("]", "")
                self.chunkHeader = self.count
                self.messageFull = self.messageFull[self.headerSize:]
                self.header = await self.onHeader({'header': self.header})  
                
                arrayHeader = self.header.split("_")
                if len(arrayHeader) >=2:
                    self.action=arrayHeader[0]
                    self.language=arrayHeader[1]
                    
                    result = await self.onAction({'action': self.action, 'language':self.language})  
                          
                return True
            else:
                return False
        
        return True
# --------------------------------------------------------------------------------------------------------------------------------------- 
    """doParser
    
    """
    async def doParser(self, message:str|Any) -> EApiText: 
        
        eApiText = EApiText()
        self.eApiText= eApiText
        eApiText.doGenerateID(f"{self.prefixID}{self.count}"  )
        messageChunk=message
        self.totenTot +=1
        eApiText.tokenTot = self.totenTot

        if message is None:
            result = await self.onDone({'fullText': self.messageFull})
            eApiText.isComplete = True
            return eApiText 
        else:
            if await self.isHeaderComplete(message):
                eApiText.header = self.header
                if self.isRemoveHeader:
                    if self.count == self.chunkHeader:
                        messageChunk = message.replace(self.header, "")
        
        result = await self.onChunk({'chunk': messageChunk})            
        
        eApiText.text = result# messageChunk
        self.count +=1
        return eApiText
    
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def onStart(self, kwargs) -> str:
        """onStart
        Args:
            kwargs (_type_): userMessage

        Returns:
            str: _description_
        """
        return await self.__doNotify('onStart', **kwargs)   
        
    async def onHeader(self, kwargs) -> str:
        return await self.__doNotify('onHeader', **kwargs) 
    
    async def onAction(self, kwargs) -> str:
        return await self.__doNotify('onAction', **kwargs) 
    
    async def onChunk(self, kwargs) -> str:
        return await self.__doNotify('onChunk', **kwargs) 
    
    async def onError(self, kwargs) -> str:
        return await self.__doNotify('onError', **kwargs) 
    
    async def onDone(self, kwargs) -> str:
        return await self.__doNotify('onDone', **kwargs) 

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doNotify(self, event_name, **kwargs) -> str:
        
        if event_name in self.mapCallback.keys():
            #print("event_name cache")
            local_vars = {'self': self}
            local_vars.update(kwargs)
            func_args = {k: local_vars[k] for k in ['self'] + list(kwargs.keys())}
           
            result = await self.mapCallback[event_name](**func_args)
            return result
        
        elif event_name in self.config['callback']:
            code = self.config['callback'][event_name]
            if self.languageAssistant == 'python':
                local_vars = {'self': self}
                local_vars.update(kwargs)
                
                # Wrap the code in a function that returns the result
                wrapped_code = f"""
async def __temp_func(self, {', '.join(kwargs.keys())}):
{textwrap.indent(code, '    ')}
    return result
"""           
                exec(wrapped_code, globals(), local_vars)
                
                # Create a dictionary with the expected arguments including 'self'
                func_args = {k: local_vars[k] for k in ['self'] + list(kwargs.keys())}
                
                result = await local_vars['__temp_func'](**func_args)
                self.mapCallback[event_name] = local_vars['__temp_func']
                return result
            else:
                raise Exception(f"ERROR_UNSUPPORTED_LANGUAGE|{self.languageAssistant}")
        else:
            raise Exception(f"ERROR_UNKNOW_EVENT|{event_name}")
# ---------------------------------------------------------------------------------------------------------------------------------------
