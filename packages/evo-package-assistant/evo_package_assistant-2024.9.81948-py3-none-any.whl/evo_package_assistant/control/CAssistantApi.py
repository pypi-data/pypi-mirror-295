#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_assistant.entity import *
from evo_package_assistant.utility import *
from evo_framework.core.evo_core_api.entity.EApiQuery import EApiQuery

# ---------------------------------------------------------------------------------------------------------------------------------------
# CAssistantApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""CAssistantApi
"""
class CAssistantApi(CApi):
	__instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self):   
		if CAssistantApi.__instance != None:
			raise Exception("ERROR:SINGLETON")
		else:
			super().__init__()
			CAssistantApi.__instance = self
			self.currentPath = os.path.dirname(os.path.abspath(__file__))
			
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""getInstance Singleton

	Raises:
		Exception:  api exception

	Returns:
		_type_: CAssistantApi instance
	"""
	@staticmethod
	def getInstance():
		if CAssistantApi.__instance is None:
			cObject = CAssistantApi()  
			cObject.doInit()  
		return CAssistantApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doInit

	Raises:
		Exception: api exception

	Returns:

	"""   
	def doInit(self):   
		try:			
			UAssistantApi.getInstance().doInit()
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise	  
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doAddApi

	Raises:
		Exception: api exception

	Returns:

	"""
	@override   
	def doAddApi(self):
		try:			
			
			api0 = self.newApi("assistant-set", callback=self.onSet, input=EAssistantAdmin, output=EAssistant )
			api0.description="assistant-set description"
			api0.required="*"

			api1 = self.newApi("assistant-get", callback=self.onGet, input=EApiQuery, output=EAssistant )
			api1.description="assistant-get description"
			api1.required="*"

			api2 = self.newApi("assistant-del", callback=self.onDel, input=EAssistantAdmin, output=EAssistant )
			api2.description="assistant-del description"
			api2.required="*"

			api3 = self.newApi("assistant-query", callback=self.onQuery, input=EApiQuery, output=EAssistantMap )
			api3.description="assistant-query description"
			api3.required="*"
  
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onSet api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onSet(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onSet: {eAction} ")

					
			async for eActionOutput in UAssistantApi.getInstance().doOnSet(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onGet api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGet(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGet: {eAction} ")

					
			async for eActionOutput in UAssistantApi.getInstance().doOnGet(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onDel api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onDel(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onDel: {eAction} ")

					
			async for eActionOutput in UAssistantApi.getInstance().doOnDel(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onQuery api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onQuery(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onQuery: {eAction} ")

					
			async for eActionOutput in UAssistantApi.getInstance().doOnQuery(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------
